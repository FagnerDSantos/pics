# Tarefa 001: Estrutura Inicial do Projeto (Full-Stack)

## Objetivo
Criar a estrutura base do monorepo para a aplicação Pics, contendo a fundação do Backend (FastAPI) e do Frontend (Next.js).

## Contexto
O projeto utilizará uma arquitetura desacoplada:
- **Backend:** Python com FastAPI para regras de negócio, endpoints e manipulação de dados.
- **Frontend:** Next.js (App Router) com TypeScript, Tailwind CSS e componentes shadcn/ui.

## Critérios de Aceite
- [ ] Criar diretório `backend/` com `main.py` (FastAPI básico) e `requirements.txt` (incluindo `fastapi`, `uvicorn`, `pydantic`, `psycopg2-binary` ou `sqlite`).
- [ ] Criar diretório `frontend/` com a estrutura base do Next.js (App Router, Tailwind e TypeScript).
- [ ] Criar um arquivo `.gitignore` na raiz ignorando `venv/`, `node_modules/`, `.env`, `__pycache__`, `.next/`.
- [ ] Criar um `README.md` atualizado documentando como rodar o backend e o frontend.

## Arquivos Permitidos
- `backend/**`
- `frontend/**`
- `.gitignore`
- `README.md`

## Fora de Escopo
- Implementação de regras complexas de autenticação, pagamentos ou upload real de fotos nesta etapa.

## Como Testar
- Validar que o backend sobe via uvicorn em `/docs`.
- Validar que o frontend compila e renderiza a página inicial.