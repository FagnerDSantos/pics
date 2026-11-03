# Tarefa 005B — Fundação multi-tenant (RLS, roles, contexto)

> **STATUS: APROVADA pelo Fagner em 03/11/2026 (todas as decisões abaixo, com as recomendações do `postgres-dba`)**
>
> Este rascunho documenta uma proposta de escopo e decisões pendentes. A autorização geral para iniciar trabalho de fundação **não substitui aprovação explícita** das decisões de schema, roles, privilégios e policies listadas na seção `Decisões para aprovação explícita`. Não implementar antes da aprovação.

## Objetivo

Criar a base multi-tenant no banco PostgreSQL para a plataforma Pics: tabelas `studios` e `studio_members`, coluna `studio_id` no `audit_log`, roles separadas para runtime e migrações, RLS fail-closed, helper de contexto bind-safe e testes sintéticos de isolamento entre estúdios.

## Contexto

- A tarefa 005 (`docs/tasks/005-postgresql-sqlalchemy-alembic.md`) entregou `users`, `sessions` e `audit_log` com Alembic, SQLAlchemy 2 e proteção append-only do `audit_log`.
- `docs/PLANO-MESTRE.md` define o isolamento entre estúdios como risco nº 1 e exige `studio_id` em toda tabela de negócio, RLS, role de banco sem `BYPASSRLS` e testes de isolamento.
- Uma consulta textual do DBA foi registrada em `docs/RETOMADA.md` recomendando: RLS fail-closed, `WITH CHECK` que rejeite `NULL`/contexto inválido, role de runtime sem `BYPASSRLS` e não-owner, contexto transacional `SET LOCAL` bind-safe, e testes A/B de leitura/escrita/UPDATE/DELETE cruzados.
- Esta task é **foundation only**: altera schema, models, roles/policies e testes; não implementa auth, rotas, frontend, seeds de dados reais nem backfill.

## Classificação de tabelas proposta (do Plano Mestre)

| Tabela | Tipo | `studio_id` | Observação |
|---|---|---|---|
| `users` | Global | `NULL` (não existe) | Conta de login da plataforma; pode estar em vários estúdios via `studio_members`. |
| `sessions` | Global | `NULL` (não existe) | Sessão de autenticação vinculada a `users.id`. |
| `studios` | Raiz do tenant, com RLS `id = ctx` + FORCE | `id` próprio | Não tem `studio_id`. Criação e listagem pré-contexto só pelas funções definer abaixo. |
| `studio_members` | Tenant | `NOT NULL` | Vínculo entre `users` e `studios`; PK/unique a decidir. |
| `audit_log` | Mista | `NULL` permitido | `NULL` para eventos da plataforma; `NOT NULL` preenchido para eventos de um estúdio. Permanece append-only. |

## Decisões para aprovação explícita

Antes de qualquer implementação, o usuário deve aprovar cada item:

- [ ] Confirmar a classificação acima (global/tenant/mista) e o fato de `audit_log.studio_id` aceitar `NULL` para eventos da plataforma.
- [ ] Escolher a PK/unique de `studio_members`: `(studio_id, user_id)` como PK composta, ou surrogate `id` com unique composta `(studio_id, user_id)`.
- [ ] Definir a role de migração (`pics_migration` ou similar) e se ela pode ter `BYPASSRLS` e/ou ownership dos objetos. Recomendação técnica: role de migração separada, não usada pela aplicação; `BYPASSRLS` é uma opção, não decisão.
- [ ] Definir a role de runtime (`app_runtime` ou similar): sem `SUPERUSER`, sem `BYPASSRLS`, não owner das tabelas, com grants mínimos explícitos (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `USAGE`, `SEQUENCE`) apenas nos objetos aprovados.
- [ ] Definir as policies RLS: `ENABLE ROW LEVEL SECURITY` + `FORCE ROW LEVEL SECURITY` nas tabelas tenant; comportamento quando `app.studio_id` está ausente, vazio ou inválido (leitura retorna vazio vs erro; escrita deve retornar erro). Recomendação técnica: fail-closed — leitura vazia, escrita erro.
- [ ] Decidir se o enforcement de membership (por exemplo, `studio_members.role IN ('studio_owner', 'studio_member', 'assembler')` e FK para `studios`/`users`) será implementado nesta fase ou deferido para a tarefa 007 (RBAC e autorização).
- [ ] Aprovar a estratégia de backup/rollback: aplicação das migrações somente no banco descartável `pics_test`; nenhuma alteração em produção, staging ou banco com dados reais.

## Critérios de aceite

- [ ] Criar migração incremental `backend/alembic/versions/0003_multi_tenant_foundation.py` (não editar `0001` nem `0002`).
  - Criar tabela `studios` com campos mínimos: `id`, `name`, `slug` (único), `status`, `created_at`.
  - Criar tabela `studio_members` vinculando `studios.id` e `users.id`; `studio_id NOT NULL`; `user_id NOT NULL`; campo `role` (valores a definir na aprovação).
  - Adicionar `audit_log.studio_id` (nullable, FK para `studios.id` com `ON DELETE RESTRICT`: SET NULL dispararia UPDATE e o trigger append-only levantaria `55000`), com índice adequado.
  - Preservar trigger append-only de `audit_log`; garantir que a nova coluna não quebre a proteção contra `UPDATE`/`DELETE`.
- [ ] Atualizar models SQLAlchemy: `Studio`, `StudioMember` e `AuditLog` com `studio_id`.
- [ ] Criar helper de contexto em `backend/app/core/tenancy.py` (ou local aprovado) para executar `SET LOCAL app.studio_id = ...` de forma bind-safe, com reset/transação curta e compatível com pooling de conexões.
- [ ] Criar roles e policies RLS (após aprovação das decisões):
  - `app_runtime` sem `SUPERUSER`/`BYPASSRLS`, não owner, com grants mínimos.
  - Role de migração separada; decisão de `BYPASSRLS`/ownership como item aprovado.
  - `ALTER TABLE ... ENABLE ROW LEVEL SECURITY; ALTER TABLE ... FORCE ROW LEVEL SECURITY;` nas tabelas aprovadas (`studios`, `studio_members`; `audit_log` conforme decisão).
  - Policies fail-closed: `WITH CHECK` rejeita `NULL`/inválido; leitura sem contexto retorna vazio (recomendado) ou erro (se aprovado).
- [ ] Testes sintéticos de integração PostgreSQL em `pics_test`:
  - Leitura/escrita/UPDATE/DELETE cruzados entre estúdios A e B devem ser isolados.
  - Contexto ausente, vazio e inválido devem ser rejeitidos/vazios conforme política aprovada.
  - Rollback/transação e reutilização de conexão devem resetar o contexto.
  - `audit_log` permanece append-only; UPDATE/DELETE continuam levantando SQLSTATE `55000`.
  - Não criar tabelas de negócio extras só para teste. Testes reais de FK cruzada (tenant → tenant) ficam diferidos até existir relação real; não declarar satisfeito.
- [ ] **Revisão do `postgres-dba` (03/11/2026), a incorporar antes da aprovação:**
  - Funções pré-contexto (§8 regra 8, S-40, D-32) na 0003, em SQL puro: `public.resolve_user_studios(p_user_id uuid) RETURNS TABLE(studio_id uuid, role text)` e `public.create_studio(p_name text, p_slug text, p_owner_user_id uuid) RETURNS uuid` (estúdio + vínculo `studio_owner` atômicos). `resolve_client_token` e `resolve_payment_ref` ficam diferidas para as tarefas que criarem `client_access` e `payments`, cada uma com função e teste.
  - Todas `SECURITY DEFINER`, `SET search_path = pg_catalog, pg_temp`, objetos qualificados com `public.`, dono `pics_resolver` (NOLOGIN, sem BYPASSRLS/SUPERUSER) com policy própria (FORCE RLS vale também para o dono), `REVOKE ALL ... FROM PUBLIC; GRANT EXECUTE ... TO app_runtime`, retorno só de identificadores e papel.
  - Testes das funções: usuário sem vínculo devolve vazio; `app_runtime` sem contexto não lê `studio_members`; `PUBLIC` sem EXECUTE; conferir `prosecdef`, `proconfig`, `proowner`; `search_path` hostil não altera o resultado.
  - `audit_log`: FK `ON DELETE RESTRICT`; índice `(studio_id, at)`; SELECT `studio_id = ctx`; INSERT `studio_id = ctx`, e `studio_id IS NULL` só por função definer `audit_platform_event(...)`; grants `SELECT, INSERT` apenas; trigger `BEFORE TRUNCATE` com `55000`. (A regra "WITH CHECK nunca aceita NULL" vale para tabelas tenant, não para esse caso mista.)
  - `studios`: CHECK em `status` e formato do `slug`, `created_at timestamptz`; `plan_id` diferido até existir `plans`. `studio_members`: PK composta `(studio_id, user_id)`, FKs com CASCADE documentado, índice em `user_id`, CHECK de `role` (schema, não RBAC).
  - Papéis `pics_migration`, `app_runtime`, `pics_resolver` criados por script em `infra/` (e passo do CI), nunca na migração; a 0003 só faz GRANT/REVOKE, sem `DROP ROLE`; `alembic/env.py` usa `pics_migration`; `ALTER DEFAULT PRIVILEGES` para tabelas futuras. Se as tabelas de 0001/0002 tiverem outro dono, trocar o dono exige aprovação do Fagner.
  - `tenancy.py`: validar `uuid.UUID`, `SELECT set_config('app.studio_id', :sid, true)` com bind, reaplicar a cada transação (evento `after_begin`), pois o `commit` zera o contexto. Policy lê `NULLIF(current_setting('app.studio_id', true), '')::uuid`; ausente/vazio = zero linhas; valor malformado = erro de cast (documentado).
  - Testes de isolamento em `backend/tests/isolation/`, conectando como `app_runtime` (afirmar `rolbypassrls=false`, `rolsuper=false`, não dono; o PostgreSQL do CI é superusuário). Cobrir A/B em SELECT, INSERT com `studio_id` de B, UPDATE trocando `studio_id`, DELETE, contexto ausente/vazio/inválido, reuso de conexão (`pool_size=1`), rollback e commit no meio da requisição.
  - Observações para `docs/reviews/` (fora desta tarefa): `audit_log.actor_id` em 0001 tem o mesmo conflito de FK SET NULL com o append-only; `users.role` (0001) diverge de `platform_role` (§10); `resolve_user_studios` deve receber `user_id` só da sessão (tarefa 006); downgrade com `DROP COLUMN` seria "contract" em produção.
- [ ] `ruff check app tests`, `mypy app`, `pytest` (com PostgreSQL em `pics_test`) e `git diff --check` passam.
- [ ] Atualizar `docs/reviews/005B-fundacao-multi-tenant-rls.md`, `docs/PLANO-MESTRE.md` (seção 20) e `docs/RETOMADA.md`.

## Arquivos que podem ser alterados

- `backend/alembic/versions/0003_multi_tenant_foundation.py` (novo)
- `backend/app/models/studio.py` (novo)
- `backend/app/models/studio_member.py` (novo)
- `backend/app/models/audit_log.py` (acrescentar `studio_id`)
- `backend/app/models/__init__.py`
- `backend/app/core/tenancy.py` (novo helper de contexto)
- `backend/app/db/session.py` (se necessário para integrar contexto bind-safe)
- `backend/tests/test_multi_tenant.py` (novo; dados sintéticos)
- `backend/tests/test_database.py` (se necessário ajustar para `studio_id` no `audit_log`)
- `.github/workflows/ci.yml` (somente se necessário para role/policy extra em CI)
- `docs/tasks/005B-fundacao-multi-tenant-rls.md`
- `docs/reviews/005B-fundacao-multi-tenant-rls.md`
- `docs/PLANO-MESTRE.md`
- `docs/RETOMADA.md`
- `backend/alembic/env.py`, `backend/tests/conftest.py`, `backend/tests/isolation/`, `infra/` (script de papéis), `docs/adr/ADR-007-*.md`

## Fora de escopo

- Autenticação, login, logout, sessão, argon2id, CSRF, rate limiting (tarefa 006).
- RBAC completo, autorização por recurso, acesso de suporte, logging estruturado (tarefa 007).
- 2FA TOTP (tarefa 008).
- Acesso do cliente final, consentimentos (tarefa 009).
- Tabelas de negócio de galerias, fotos, clientes, pagamentos etc.
- Frontend, rotas, schemas Pydantic de API.
- Backfill de dados reais; aplicação em produção/staging.
- Alterar migrações `0001_initial` ou `0002_audit_log_append_only`.
- Commit/push até aprovação da spec e revisão do diff.

## Regras de segurança aplicáveis

- Usar apenas dados sintéticos em testes, logs e prompts; nunca ler `.env`, segredos, fotos reais ou dados pessoais.
- A role de runtime (`app_runtime`) não deve ter `SUPERUSER`, `BYPASSRLS` nem ser owner dos objetos.
- Grants mínimos explícitos; nunca dar `ALL PRIVILEGES` de forma irrestrita.
- RLS fail-closed: policies devem negar acesso quando o contexto de estúdio está ausente, vazio ou inválido.
- `WITH CHECK` de policies de escrita nunca pode aceitar `NULL` como válido.
- Contexto de estúdio por requisição via `SET LOCAL app.studio_id` (ou equivalente bind-safe), transação curta, compatível com pooling.
- `audit_log` permanece append-only; UPDATE/DELETE proibidos.
- Aplicação das migrações limitada ao banco descartável `pics_test`; nenhum banco de produção/staging/dados reais.

## Como testar

1. Aprovar explicitamente as decisões desta spec.
2. Iniciar PostgreSQL 16 em contêiner isolado, banco `pics_test`, com `DATABASE_URL` sintético por variável de ambiente.
3. Executar `alembic upgrade head`, validar tabelas/constraints/policies; depois `alembic downgrade base` e `alembic upgrade head`.
4. Executar testes de integração PostgreSQL com roles sintéticas (`app_runtime` etc.).
5. Executar `ruff check app tests`, `mypy app`, `pytest` e `git diff --check`.
6. Confirmar que containers/volumes temporários foram removidos e que nenhum dado real foi tocado.

## Relatório do executor (preenchido pelo Claude Code)

- O que foi feito:
- Arquivos alterados:
- Dúvidas ou riscos:
