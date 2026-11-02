# Pics

Galeria de fotos. Monorepo com backend em FastAPI e frontend em Next.js. A tela
atual é uma prévia demonstrativa com dados fictícios.

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
  docker-compose.yml  # PostgreSQL, MinIO e Mailpit para desenvolvimento
docs/adr/             # decisões arquiteturais em proposta
```

## Pré-requisitos

- Python 3.12 (recomendado; 3.11 a 3.13 suportados)
- Node.js 20+
- Docker Compose (opcional, para os serviços locais)

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

Variáveis do backend: copie `backend/.env.example` para `backend/.env` e ajuste
os valores locais. Os serviços do Compose leem `.env` na raiz; use os valores
fictícios de `.env.example` como ponto de partida. Esses valores são somente
para desenvolvimento local.

### Serviços locais

```bash
docker compose -f infra/docker-compose.yml up -d
```

Antes de subir os serviços, copie `.env.example` para `.env` (PowerShell:
`Copy-Item .env.example .env`; bash: `cp .env.example .env`).

| Serviço | Endereço local | Porta padrão |
| --- | --- | ---: |
| PostgreSQL | `127.0.0.1` | 5432 |
| MinIO API | `http://127.0.0.1:9000` | 9000 |
| MinIO Console | `http://127.0.0.1:9001` | 9001 |
| Mailpit SMTP | `127.0.0.1` | 1025 |
| Mailpit UI | `http://127.0.0.1:8025` | 8025 |

As portas e credenciais locais podem ser configuradas pelas variáveis listadas
em `.env.example`. Não reutilize os valores fictícios em outros ambientes.

### Qualidade e testes

```bash
cd backend
ruff check app tests
mypy app
pytest
```

## Frontend

```bash
cd frontend
npm ci
npm run dev
```

A aplicação fica disponível em `http://localhost:3000`.

### Qualidade

```bash
cd frontend
npm run lint
npm run typecheck
npm run build
npm audit --audit-level=high
```

## Segredos e configuração

- `.env` e arquivos de ambiente locais não devem ser versionados; `.env.example`
  contém apenas valores fictícios.
- O hook opcional de pre-commit usa uma instalação local de Gitleaks. CI também
  executa a varredura de segredos; configure Gitleaks localmente para usar o hook.
- O CI executa os checks do backend, `npm ci`, lint, TypeScript, build e `npm audit --audit-level=high`
  e varredura de segredos.

## Endereços da aplicação

| Serviço | Endereço |
| --- | --- |
| Backend | `http://localhost:8000` |
| Documentação da API | `http://localhost:8000/docs` |
| Frontend | `http://localhost:3000` |
