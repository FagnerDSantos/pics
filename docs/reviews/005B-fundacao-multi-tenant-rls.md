# Relatório 005B — Fundação multi-tenant (RLS, papéis, contexto)

Concluída em 03/11/2026 (Claude Code, Sonnet). Spec e decisões aprovadas pelo Fagner (ADR-007, D-32).

## O que foi feito
- Migração `0003_multi_tenant_foundation`: `studios`, `studio_members` (PK composta), `audit_log.studio_id` (FK `RESTRICT`, índice `(studio_id, at)`, trigger `BEFORE TRUNCATE` com `55000`), `public.current_studio_id()`.
- RLS `ENABLE` + `FORCE` em `studios`, `studio_members` e `audit_log`. Contexto ausente/vazio = zero linhas (escrita rejeitada); valor malformado = erro de cast (`22P02`), fail-closed.
- Papéis em `infra/postgres/roles.sql` (fora da migração; montado no compose para volume novo): `pics_migration` (dono), `app_runtime` (sem SUPERUSER/BYPASSRLS, não dono), `pics_resolver` (NOLOGIN, dono das funções definer). A 0003 só faz GRANT/REVOKE.
- Funções definer (`search_path = pg_catalog, pg_temp`, sem EXECUTE para PUBLIC, dono `pics_resolver`): `resolve_user_studios`, `create_studio`, `audit_platform_event` (ação restrita a `platform.*`, `meta` ≤ 4 KB).
- `app/core/tenancy.py`: `set_studio_context` (bind, só `UUID`, reaplicado em `after_begin` porque o commit zera o contexto), `clear_studio_context`, wrappers das funções.
- `alembic/env.py` usa `MIGRATION_DATABASE_URL` se existir, senão `DATABASE_URL`. Os testes migram como `pics_migration` (não superusuário), o caminho real.
- Testes: `backend/tests/isolation/test_multi_tenant.py` (conecta como `app_runtime`, pool de 1 conexão). A/B em SELECT, INSERT, UPDATE (inclusive trocar `studio_id`), DELETE; contexto ausente/vazio/inválido; vazamento por pool, commit e rollback; funções (metadados, `search_path` hostil, estúdio suspenso, slug inválido); `audit_log` (isolamento, append-only, TRUNCATE, FK).
- Desvio de caminho: o teste ficou em `tests/isolation/` (permitido na lista), não em `tests/test_multi_tenant.py`.

## Decisões de implementação
- **Sem `ALTER DEFAULT PRIVILEGES`:** grants explícitos por tabela (menor privilégio); tabelas futuras recebem grants na própria migração.
- **Grants de `app_runtime`:** `studios` só `SELECT` e `UPDATE (name)` (status, slug e id são da plataforma); `studio_members` só `SELECT` (escrita e papéis na 007). Os testes concedem escrita a `studio_members` só no banco de teste, para provar que a RLS bloqueia escrita cruzada.
- `resolve_user_studios` devolve só estúdios `active`.

## Checks
`ruff check app tests`, `mypy app`, `pytest` (26 testes em PostgreSQL 16 `pics_test`), `git diff --check`: verdes. `alembic upgrade head` como `pics_migration` e `downgrade base`/`upgrade head` verificados.

## Diferido / fora do escopo
- Teste real de FK cruzada tenant→tenant: não existe relação tenant→tenant ainda; **não satisfeito**, fica para a primeira tabela com FK composta.
- `resolve_client_token` e `resolve_payment_ref`: entregues com `client_access` (009) e `payments` (016a), cada uma com teste.
- Volume Docker antigo não executa `roles.sql`: rode `psql -U <superusuário> -d <banco> -f infra/postgres/roles.sql` e defina senhas com `ALTER ROLE ... PASSWORD` fora do repositório; sem os papéis a 0003 falha com mensagem clara.

## Observações para tarefas futuras (não corrigidas aqui)
1. `audit_log.actor_id` (0001) tem FK `ON DELETE SET NULL`, o mesmo conflito com o append-only; trocar para `RESTRICT`/anonimizar.
2. `users.role` (`admin/assembler/client`) diverge de `platform_role` do plano §10; dois lugares com papel (`users.role` e `studio_members.role`).
3. **Tarefa 006/007:** `resolve_user_studios`, `create_studio` e `audit_platform_event` aceitam `user_id`/`actor_id` como argumento; a API só pode passar o `user_id` da sessão autenticada. Avaliar GUC `app.user_id` definido pelo servidor para que o banco confira o usuário. Rate limit e cota de criação de estúdios na aplicação; erro de slug duplicado revela slugs existentes.
4. **`users` e `sessions` são globais (sem RLS)** e `app_runtime` tem SELECT/UPDATE nelas: uma injeção SQL ou IDOR lê hashes de qualquer usuário. Na 006: guardar só hash do token de sessão, grants por coluna, avaliar RLS por `app.user_id`. Registrar na ADR-007 que `users` é global por escolha.
5. Falhar o startup da API se o papel de conexão for `rolsuper`, `rolbypassrls` ou dono das tabelas (hoje, com `DATABASE_URL` apontando para o superusuário do compose, a RLS fica silenciosamente desligada).
6. Injeção SQL de `set_config('app.studio_id')` troca de estúdio: manter consultas sempre parametrizadas.
7. FK `audit_log → studios` com `RESTRICT` impede excluir estúdio; a eliminação LGPD deve anonimizar, não excluir.
8. O downgrade da 0003 apaga `audit_log.studio_id` (em produção seria migração "contract").
9. O dono das tabelas em ambientes existentes deve ser `pics_migration`; trocar o dono de objetos já criados por outro papel exige aprovação do Fagner.

## Revisões (change-reviewer, postgres-dba, security-reviewer)
Sem bloqueadores. Aplicado na rodada de correção: `UPDATE (name)` em `studios` e `studio_members` só leitura; validação de ação (`platform.*`) e tamanho de `meta` em `audit_platform_event`; migração testada como `pics_migration`; `RuntimeError` no lugar de `assert`; testes de catálogo (RLS forçada em toda tabela de tenant), de privilégios mínimos e do dono do `audit_log`. Não aplicado, por decisão: `(SELECT current_studio_id())` como InitPlan (otimização), pré-check ampliado de papéis.

## Riscos de produção (dono ≠ superusuário)
- `FORCE RLS` sem policy para `pics_migration`: o dono vê zero linhas; migração futura com backfill em `studios`, `studio_members` ou `audit_log` precisa de `NO FORCE` temporário ou policy própria (pede aprovação).
- `pg_dump` como `pics_migration` sai vazio: usar papel de backup separado (superusuário ou `BYPASSRLS`), documentado.
- O dono ainda pode `DROP TRIGGER` no `audit_log` (inerente ao PostgreSQL); mitigar com `log_statement=ddl`.
- `app_runtime` pode inserir em `studio_members` apenas com o grant de teste; em produção a escrita é só da 007, que deve impedir auto-promoção a `studio_owner`.
