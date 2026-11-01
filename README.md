# Pics

Galeria de fotos. Monorepo com backend em FastAPI e frontend em Next.js.

## Estrutura

```text
backend/
  app/
    api/v1/routes/    # rotas versionadas
    core/             # configuração e utilidades centrais
    middleware/       # middlewares (ex.: headers de segurança)
  tests/
frontend/
  src/
    app/              # páginas do Next.js
    components/       # componentes reutilizáveis
    hooks/            # hooks compartilhados
    lib/              # utilitários
    services/         # clientes de API
    types/            # tipos compartilhados
infra/
  docker-compose.yml  # Postgres (tarefa de banco de dados)
```

## Pré-requisitos

- Python 3.12 (recomendado; 3.11 a 3.13 suportados)
- Node.js 20+

## Backend

```bash
cd backend
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux/macOS
# source .venv/bin/activate

pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
```

A API fica disponível em `http://localhost:8000`.
A documentação interativa fica em `http://localhost:8000/docs`.

Variáveis de ambiente: copie `backend/.env.example` para `backend/.env` e ajuste os valores.

### Qualidade e testes

```bash
cd backend
ruff check app
mypy app
pytest
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

A aplicação fica disponível em `http://localhost:3000`.

### Qualidade

```bash
cd frontend
npm run lint
npm run build
```

## Portas

| Serviço  | Porta |
| -------- | ----- |
| Backend  | 8000  |
| Frontend | 3000  |
