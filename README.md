# Pics

Galeria de fotos. Monorepo com backend em FastAPI e frontend em Next.js.

## Estrutura

- `backend/` - API em FastAPI (porta 8000)
- `frontend/` - Aplicação web em Next.js + Tailwind CSS (porta 3000)

## Pré-requisitos

- Python 3.11+
- Node.js 20+

## Backend

```bash
cd backend
python -m venv venv
# Windows (PowerShell)
venv\Scripts\Activate.ps1
# Linux/macOS
# source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

A API fica disponível em `http://localhost:8000`.
A documentação interativa fica em `http://localhost:8000/docs`.

Variáveis de ambiente: copie `backend/.env.example` para `backend/.env` e ajuste os valores.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

A aplicação fica disponível em `http://localhost:3000`.

## Portas

| Serviço  | Porta |
| -------- | ----- |
| Backend  | 8000  |
| Frontend | 3000  |
