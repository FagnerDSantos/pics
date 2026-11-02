# Tarefa 005 - PostgreSQL, SQLAlchemy 2 e Alembic

## Objetivo
Integrar PostgreSQL ao backend com SQLAlchemy 2 e Alembic, incluindo a primeira migração para `users`, `sessions` e `audit_log`. Validar o ciclo de migração e persistência com testes de integração contra PostgreSQL em contêiner.

## Contexto
- Tarefa do marco M0, prevista em `docs/PLANO-MESTRE.md`, seções 7, 8 e 14.
- Docker Desktop/WSL2 está operacional; `infra/docker-compose.yml` define PostgreSQL exposto apenas em loopback.
- O backend usa Python 3.12 e já tem `backend/pyproject.toml`, requirements fixados e testes em `backend/tests/`.
- O ADR-002 permanece proposta; a tarefa implementa a arquitetura prevista, sem alterar seu status.

## Critérios de aceite
- [x] Adicionar SQLAlchemy 2, Alembic e driver PostgreSQL oficial com versões fixadas, após validar nomes/origens oficiais; atualizar os requirements necessários sem dependências não relacionadas.
- [x] Adicionar configuração de `DATABASE_URL` por ambiente, sem credenciais reais, e engine/session SQLAlchemy 2 sincronizados com os serviços atuais do backend.
- [x] Criar `Base` declarativa e modelos `User`, `Session` e `AuditLog` conforme a seção 8 do plano mestre: UUIDs, datas `timestamptz`, campos e índices/uniqueness essenciais, role limitada a `admin`/`assembler`/`client` e dinheiro fora do escopo.
- [x] Configurar Alembic para usar a URL de ambiente e `Base.metadata`; criar migração inicial reproduzível para as três tabelas e downgrade correspondente.
- [x] Testar upgrade, downgrade/upgrade e persistência/constraints contra PostgreSQL real em contêiner usando somente dados fictícios; os testes limpam por reset do schema, sem `DELETE` direto em `audit_log`.
- [x] Impor no PostgreSQL que `audit_log` seja somente inserção, rejeitando `UPDATE` e `DELETE` por trigger e cobrindo ambos nos testes.
- [x] Não alterar rotas de produto, implementar autenticação, inserir usuários reais nem registrar segredos.
- [x] Atualizar instruções de execução/teste do backend, configurar a suíte PostgreSQL no job backend do CI e registrar relatório em `docs/reviews/005-postgresql-sqlalchemy-alembic.md`.
- [x] `ruff check app tests`, `mypy app`, `pytest` e `git diff --check` passam; testes de integração PostgreSQL executados e aprovados.

## Arquivos que podem ser alterados
- `backend/requirements.txt`
- `backend/requirements-dev.txt`
- `backend/pyproject.toml`
- `backend/.env.example`
- `backend/app/core/config.py`
- `backend/app/db/**`
- `backend/app/models/**`
- `backend/alembic.ini`
- `backend/alembic/**`
- `backend/tests/**`
- `backend/README.md` (ou documentação backend existente; não criar duplicata se houver instruções adequadas)
- `.github/workflows/ci.yml` (somente para prover PostgreSQL aos testes de integração, se necessário)
- `docs/tasks/005-postgresql-sqlalchemy-alembic.md`
- `docs/reviews/005-postgresql-sqlalchemy-alembic.md`
- `docs/PLANO-MESTRE.md`
- `docs/RETOMADA.md`

## Fora de escopo
- Autenticação, autorização, rotas de cadastro/login, seeds de usuário e dados reais.
- Novas tabelas além de `users`, `sessions` e `audit_log`; alterações de esquema sem relação com a migração inicial.
- Revisar/aprovar ADR-002 ou decisões pendentes do plano mestre.
- Mudar as credenciais ou portas do Compose, conectar serviços externos ou usar fotos/dados reais.
- Fazer commit, alterar arquivos locais do OpenCode ou acessar `.env`.

## Regras de segurança aplicáveis
- Usar apenas dados sintéticos nos testes e logs; nunca ler `.env` nem registrar credenciais locais.
- Ler `DATABASE_URL` exclusivamente do ambiente; não montar URL por concatenação insegura nem registrar a URL.
- Restringir o role por constraint no banco e emails com unicidade no banco; não armazenar token de sessão em texto claro (somente `token_hash`).
- Não expor PostgreSQL fora de `127.0.0.1`; não iniciar outros serviços do Compose além do necessário para os testes.
- Seguir S-13 do plano: consultas parametrizadas via ORM, sem SQL concatenado.

## Como testar
1. No backend, instalar as dependências fixadas de `requirements.txt` e `requirements-dev.txt` em Python 3.12.
2. Iniciar apenas o serviço postgres com Compose, aguardar healthcheck e configurar `DATABASE_URL` por variável de ambiente sem imprimir seu valor.
3. Executar Alembic upgrade, validar tabelas/constraints, downgrade e upgrade novamente; rodar testes de integração.
4. Executar `ruff check app tests`, `mypy app`, `pytest` e `git diff --check`.
5. Confirmar que containers de teste foram encerrados ao final e revisar o diff para garantir escopo e ausência de segredos.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito: adicionada migração incremental `0002_audit_log_append_only` com trigger `BEFORE UPDATE OR DELETE`; os testes confirmam que ambas as operações retornam SQLSTATE `55000` e deixam a linha intacta. A limpeza não executa `DELETE` em `audit_log`; remove o schema de teste por downgrade. Job backend do CI recebe PostgreSQL e `DATABASE_URL` sintéticos.
- Arquivos alterados: `.github/workflows/ci.yml`, `backend/README.md`, `backend/alembic/versions/0002_audit_log_append_only.py`, `backend/tests/test_database.py`, esta tarefa, `docs/PLANO-MESTRE.md`, `docs/reviews/005-postgresql-sqlalchemy-alembic.md` e `docs/RETOMADA.md`.
- Dúvidas ou riscos: validações locais aprovadas; a execução remota do GitHub Actions aguarda publicação da alteração. Nenhum commit foi feito conforme solicitado.
