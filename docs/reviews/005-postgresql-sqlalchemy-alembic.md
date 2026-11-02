# Revisão da tarefa 005 — PostgreSQL, SQLAlchemy 2 e Alembic

## Parecer

**Aprovada após correções.** A revisão encontrou que o requisito S-22 do plano mestre (`audit_log` somente inserção) não era imposto no banco. A proteção e a cobertura de integração foram implementadas e validadas localmente.

## Diagnóstico e correções

- `backend/alembic/versions/0002_audit_log_append_only.py:18` cria função PL/pgSQL e trigger `BEFORE UPDATE OR DELETE`. Cada tentativa levanta SQLSTATE `55000`. A regra foi separada da migração inicial para também ser aplicada a bancos que já registraram `0001_initial`.
- `backend/tests/test_database.py:113` e `:122` tentam atualizar e excluir a linha sintética, conferem o SQLSTATE e verificam que a auditoria permaneceu intacta.
- A limpeza não apaga linhas de `audit_log`: os dados sintéticos são descartados no downgrade do schema de teste, seguido de upgrade. A linha mantém a referência ao ator e não dispara uma atualização referencial incompatível com a imutabilidade.
- `.github/workflows/ci.yml:14` adiciona serviço PostgreSQL 16 com healthcheck e `DATABASE_URL` de uso exclusivo em CI; o job executa `ruff check app tests`, mypy e pytest.
- `backend/README.md:37` documenta a cobertura append-only e o reset de schema. A tarefa e o status do plano mestre foram atualizados.
- `backend/.env.example:1` explicita `postgresql+psycopg://`, usando o driver `psycopg` fixado em `backend/requirements.txt`.

## Pontos fortes

- A proteção é aplicada no próprio PostgreSQL, independentemente de uso do ORM.
- O downgrade remove trigger e função; o teste realiza downgrade/upgrade e verifica persistência e constraints.
- A limpeza não emite `DELETE` em `audit_log` e os testes usam exclusivamente dados fictícios.
- `DATABASE_URL` e credenciais do CI são sintéticas; `.env` não foi lido.

## Segurança

| Item | Onde | Situação |
|---|---|---|
| S-22 — `audit_log` somente inserção | `backend/alembic/versions/0002_audit_log_append_only.py:18-44`; `backend/tests/test_database.py:113-127` | Atendido: UPDATE e DELETE são bloqueados pelo PostgreSQL e testados por integração. |
| S-13 — consultas parametrizadas | `backend/tests/test_database.py:113-123` | Atendido: as tentativas usam expressões SQLAlchemy parametrizadas; SQL literal é limitado ao DDL estático da migração. |
| Segredos / arquivos locais | `.github/workflows/ci.yml:18-29`; `.env` e `.opencode/` | URL de CI fictícia; nenhum `.env` ou arquivo local OpenCode foi lido ou alterado. |

## Validações

| Comando | Resultado |
|---|---|
| `ruff check app tests` | Aprovado |
| `mypy app` | Aprovado: 20 arquivos |
| `pytest` com PostgreSQL em `pics_test` | Aprovado: 9 passaram; 1 aviso de depreciação do `TestClient`/Starlette |
| `git diff --check` | Aprovado |

O PostgreSQL de teste do projeto Compose `pics-task005` foi iniciado para os testes e removido ao final com `docker compose down -v`; não restaram containers nem volumes. O workflow foi configurado, mas sua execução remota depende da publicação das alterações. Nenhum commit foi feito, conforme solicitado.

## Próximo passo

Executar o job backend do GitHub Actions quando a alteração for publicada; revisar seu resultado remoto.
