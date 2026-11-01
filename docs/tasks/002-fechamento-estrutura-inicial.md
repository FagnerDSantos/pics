# Tarefa 002 - Fechamento da estrutura inicial

## Objetivo
Concluir os critérios de aceite pendentes da tarefa 001, deixando o monorepo pronto para receber as funcionalidades.

## Contexto
A tarefa 001 criou `backend/` (FastAPI) e `frontend/` (Next.js 16 + Tailwind v4), mas deixou pendências: `.gitignore` e `README.md` na raiz, driver de banco em `requirements.txt` e página inicial ainda no boilerplate do Next.js.

## Critérios de aceite
- [ ] Criar `.gitignore` na raiz ignorando `venv/`, `node_modules/`, `.env`, `__pycache__/`, `.next/` e `*.pyc`.
- [ ] Criar `README.md` na raiz explicando pré-requisitos, como rodar o backend (venv + `pip install -r requirements.txt` + `uvicorn main:app --reload`) e o frontend (`npm install` + `npm run dev`), e as portas usadas (8000 e 3000).
- [ ] Ajustar `backend/requirements.txt` para incluir `python-dotenv` (leitura de `.env`) e manter as versões existentes. Não adicionar driver de banco nesta tarefa (decisão adiada para a tarefa de banco de dados).
- [ ] Criar `backend/.env.example` com `DATABASE_URL` e `CORS_ORIGINS` como placeholders (sem segredos reais).
- [ ] Substituir o conteúdo de `frontend/src/app/page.tsx` por uma página inicial simples do Pics (título "Pics", texto curto e link para a documentação da API em `http://localhost:8000/docs`), usando apenas Tailwind. Sem imagens do template do Next.
- [ ] Atualizar `frontend/src/app/layout.tsx` com metadados `title: "Pics"` e `description: "Galeria de fotos"`.
- [ ] Rodar `npm run lint` e `npm run build` no frontend sem erros.
- [ ] Validar que o backend importa sem erro: `python -c "import main"` dentro de `backend/`.

## Arquivos que podem ser alterados
- `.gitignore`
- `README.md`
- `backend/requirements.txt`
- `backend/.env.example`
- `frontend/src/app/page.tsx`
- `frontend/src/app/layout.tsx`

## Fora de escopo
- Inicializar shadcn/ui (adiciona dependências novas; exige aprovação separada).
- Adicionar driver de banco (psycopg2/Postgres ou ORM).
- Autenticação, upload de fotos, pagamentos e qualquer regra de negócio.
- Alterar `backend/main.py` além do necessário.

## Regras de segurança aplicáveis
- Não incluir segredos, chaves ou dados reais em nenhum arquivo.
- `.env` deve permanecer fora do versionamento; apenas `.env.example` com placeholders.
- Não instalar dependências novas no frontend.

## Como testar
1. `backend/`: criar venv, ativar, `pip install -r requirements.txt`, `python -c "import main"`.
2. `frontend/`: `npm run lint` e `npm run build`.
3. `git status` para confirmar que `.gitignore` está funcionando (sem `node_modules/`, `.next/`, `__pycache__/`).

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito:
- Arquivos alterados:
- Dúvidas ou riscos:
