# ADR-007: Multi-tenancy com `studio_id` + RLS

- **Status:** Aprovada pelo Fagner em 03/11/2026 (junto com a D-32: funções `SECURITY DEFINER`).
- **Contexto:** Cada fotógrafo é um estúdio (tenant). Vazamento entre estúdios é o
  risco nº 1 do produto. Três fluxos chegam sem `studio_id` conhecido: link do
  cliente final, webhook do provedor de pagamento e login de usuário com vários
  estúdios (plano §8 regra 8, S-40, D-32).
- **Proposta:**
  1. **Banco único, esquema único.** Toda tabela de negócio tem `studio_id NOT NULL`
     indexado; chaves estrangeiras compostas com `studio_id` onde fizer sentido.
  2. **RLS como segunda barreira:** `ENABLE` + `FORCE ROW LEVEL SECURITY` nas tabelas
     tenant; contexto por transação com `SET LOCAL app.studio_id` (bind-safe, via
     `set_config(..., true)`). Fail-closed: contexto ausente, vazio ou inválido
     devolve zero linhas na leitura e erro na escrita (`WITH CHECK` nunca aceita
     `NULL`). A checagem na aplicação continua obrigatória.
  3. **Papéis separados:** `pics_migration` (dono dos objetos, roda Alembic, não
     usado pela API) e `app_runtime` (sem `SUPERUSER`, sem `BYPASSRLS`, não dono,
     grants mínimos explícitos). `BYPASSRLS` é proibido para a API.
  4. **Classificação:** globais (`users`, `sessions`, `plans`, `webhook_events` só com
     `payload_hash`), mista (`audit_log`, `studio_id` nulo só para eventos da
     plataforma) e tenant (todas as demais).
  5. **Resolução pré-contexto (regra 8):** funções `SECURITY DEFINER` mínimas, ex.:
     `resolve_client_token(token_hash)` e `resolve_payment_ref(provider, provider_ref)`.
     Dono sem login, `search_path` fixo (`pg_catalog, public` com objetos
     qualificados), `REVOKE ALL FROM PUBLIC` e `GRANT EXECUTE` só a `app_runtime`,
     retorno só de identificadores, teste próprio (token inválido, expirado,
     revogado, de outro estúdio). Depois a API faz `SET LOCAL app.studio_id`.
  6. **Storage:** chaves `studios/{studio_id}/...`; URL assinada só após checar
     permissão e estúdio.
- **Alternativas descartadas:** banco ou esquema por estúdio (custo operacional e de
  migração alto para o porte do beta); só filtro na aplicação (uma falha vaza dados);
  papel com `BYPASSRLS` para fluxos pré-contexto (anula a barreira).
  Alternativa em aberto para D-32: tabela global de roteamento em vez de funções
  `SECURITY DEFINER` (sugerido: funções).
- **Consequências:** toda rota nova exige teste de isolamento com dois estúdios; toda
  migração roda como `pics_migration`; testes de banco precisam de PostgreSQL real
  com os dois papéis; funções `SECURITY DEFINER` viram superfície de revisão
  obrigatória (`postgres-dba` e `security-reviewer`).
- **Revisão:** validar com o `postgres-dba` (FORCE RLS, `search_path`, grants,
  pooling com `SET LOCAL`) antes de aprovar. Aprovar junto com D-32.
