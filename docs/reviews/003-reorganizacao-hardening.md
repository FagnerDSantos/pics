# Revisão 003 - Reorganização de pastas e hardening base

## Resultado
Aprovado com ajustes menores aplicados pelo revisor.

## Critérios de aceite
- [x] Backend movido para `backend/app/` (`main.py`, `api/v1/router.py`, `api/v1/routes/health.py`, `core/config.py`) e `backend/main.py` removido.
- [x] `core/config.py` lê `.env` via `python-dotenv`, expõe `cors_origins` e `app_version`, sem segredos.
- [x] CORS a partir de `CORS_ORIGINS`, métodos explícitos e headers `Authorization`/`Content-Type` (sem `*`).
- [x] Headers de segurança em todas as respostas (`nosniff`, `DENY`, `Referrer-Policy`, `Permissions-Policy`).
- [x] `GET /` e `GET /health` com o mesmo contrato, agora em `app/api/v1/routes/health.py`.
- [x] Execução via `uvicorn app.main:app --reload`, README atualizado.
- [x] `backend/pyproject.toml` (ruff/mypy/pytest) e `backend/requirements-dev.txt` com versões fixas.
- [x] `backend/tests/test_health.py` cobrindo `/`, `/health` e headers.
- [x] Camadas do frontend criadas com `.gitkeep`; `frontend/README.md` aponta para a raiz.
- [x] Assets de boilerplate removidos (`file`, `globe`, `next`, `vercel`, `window`).
- [x] `.editorconfig`, `.gitignore` ampliado, `infra/docker-compose.yml` e `.github/workflows/ci.yml`.
- [x] Validações executadas pelo revisor (abaixo).

## Validações do revisor
| Comando | Resultado |
|---|---|
| `ruff check app` (venv 3.12) | OK |
| `mypy app` | OK (11 arquivos) |
| `pytest` | 3 passed |
| `npm run lint` | OK |
| `npm run build` | OK |
| `git check-ignore` | `.venv/`, caches, `.next/`, `node_modules/`, `.env` e `.env.*` ignorados; `.env.example` versionável |

## Ajustes aplicados pelo revisor
- `README.md:28`: pré-requisito alterado para "Python 3.12 (recomendado; 3.11 a 3.13 suportados)" — o `pydantic==2.10.4` fixado não tem wheel para Python 3.14.
- `.gitignore`: adicionados `.env.*` e `!.env.example` para bloquear variantes de ambiente sem perder o exemplo.

## Observações para as próximas tarefas
- `pydantic==2.10.4`/`fastapi==0.115.6` não instalam em Python 3.14; atualizar versões na tarefa 004 ou antes.
- CI usa `npm install` porque não há `package-lock.json` versionado; versionar o lockfile e migrar para `npm ci` em tarefa futura.
- `infra/docker-compose.yml` exige `POSTGRES_USER`, `POSTGRES_PASSWORD` e `POSTGRES_DB` definidos; criar `.env` de infra na tarefa 004.
- Respostas de preflight CORS (OPTIONS) não recebem os headers de segurança, pois o CORS responde antes do middleware interno. Impacto baixo; corrigir se necessário.
- `pyproject.toml` declara `requires-python = ">=3.11"`; alinhar com a faixa realmente suportada (3.11–3.13).

## Ajustes necessários
Nenhum bloqueante.
