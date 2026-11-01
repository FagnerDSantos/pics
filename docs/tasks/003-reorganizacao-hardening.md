# Tarefa 003 - Reorganização de pastas e hardening base

## Objetivo
Reorganizar o monorepo segundo boas práticas (backend em pacote `app/`, frontend em camadas, arquivos de raiz) e aplicar a base de segurança (CORS via ambiente, headers HTTP, ferramentas de qualidade), sem alterar regras de negócio e sem banco de dados.

## Contexto
Estado atual: `backend/main.py` concentra tudo; frontend usa apenas `src/app` e assets de boilerplate; raiz sem `.editorconfig`, CI, `infra/` ou `requirements-dev.txt`. Tarefas 001 e 002 concluídas.

## Critérios de aceite
- [ ] Mover backend para o pacote `backend/app/` com `main.py`, `api/v1/router.py`, `api/v1/routes/health.py` e `core/config.py`. `main.py` da raiz de `backend/` deve ser removido.
- [ ] `core/config.py` lê `.env` via `python-dotenv` e expõe `cors_origins` (lista separada por vírgula, padrão `http://localhost:3000`) e `app_version`. Sem segredos no código.
- [ ] CORS configurado a partir de `cors_origins`, com `allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"]` e `allow_headers=["Authorization", "Content-Type"]`. Não usar `*` em métodos/cabeçalhos.
- [ ] Middleware de headers de segurança: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy: geolocation=(), camera=(), microphone=()`.
- [ ] Manter os endpoints `GET /` e `GET /health` com o mesmo contrato atual, agora em `app/api/v1/routes/health.py`.
- [ ] Backend passa a rodar com `uvicorn app.main:app --reload`; atualizar `README.md` da raiz.
- [ ] Criar `backend/pyproject.toml` com configuração de `ruff`, `mypy` e `pytest`; criar `backend/requirements-dev.txt` com `pytest`, `httpx`, `ruff` e `mypy`.
- [ ] Criar `backend/tests/test_health.py` cobrindo `GET /` e `GET /health` via `fastapi.testclient`.
- [ ] Frontend: criar `src/components/`, `src/lib/`, `src/hooks/`, `src/types/` e `src/services/` (com `.gitkeep`). Substituir `frontend/README.md` por um ponteiro para o README da raiz.
- [ ] Remover assets de boilerplate não usados: `frontend/public/{file,globe,next,vercel,window}.svg`.
- [ ] Raiz: criar `.editorconfig`, ampliar `.gitignore` (`*.venv`, `.venv/`, `dist/`, `coverage/`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`, `*.log`) e criar `infra/docker-compose.yml` com serviço `postgres:16-alpine` usando variáveis `${POSTGRES_*}` (sem senha fixa), sem subir banco nesta tarefa.
- [ ] Criar `.github/workflows/ci.yml` com jobs de backend (ruff, mypy, pytest) e frontend (lint, build).
- [ ] Validações: `ruff check app`, `mypy app`, `pytest`, `npm run lint`, `npm run build` sem erros.

## Arquivos que podem ser alterados
- `backend/**` (inclui remoção de `backend/main.py`)
- `frontend/src/**`
- `frontend/README.md`
- `frontend/public/file.svg`, `globe.svg`, `next.svg`, `vercel.svg`, `window.svg` (remoção)
- `.editorconfig`
- `.gitignore`
- `README.md`
- `infra/docker-compose.yml`
- `.github/workflows/ci.yml`

## Fora de escopo
- Postgres, SQLAlchemy, Alembic, modelos e migrações (tarefa 004).
- Autenticação, autorização, upload de fotos, pagamentos.
- shadcn/ui e qualquer dependência nova de runtime no frontend.
- Alterar contratos de API além da mudança de caminho interno.

## Regras de segurança aplicáveis
- Nenhum segredo, chave ou dado real em código, compose ou CI.
- `.env` continua ignorado; apenas `.env.example` com placeholders.
- CORS sem `*` em métodos e cabeçalhos.
- Headers de segurança obrigatórios em todas as respostas.
- Dependências de desenvolvimento fixadas em `requirements-dev.txt`.

## Como testar
1. `cd backend`: `pip install -r requirements.txt -r requirements-dev.txt`, `ruff check app`, `mypy app`, `pytest`.
2. `uvicorn app.main:app --reload` e abrir `http://localhost:8000/docs`.
3. `cd frontend`: `npm run lint` e `npm run build`.
4. `git status` para confirmar que `__pycache__/`, `.pytest_cache/`, `.mypy_cache/` e `.ruff_cache/` estão ignorados.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito:
- Arquivos alterados:
- Dúvidas ou riscos:
