# Tarefa 003B - Hardening restante e atualização de pins

## Objetivo
Concluir as pendências registradas para a tarefa 003: limite do corpo HTTP e respostas de erro que não exponham dados internos. Atualizar os pins de runtime para as versões já instaladas e validadas no ambiente global, sem adicionar dependências.

## Contexto
- `docs/PLANO-MESTRE.md` seção 18 marca a tarefa 003 como parcial por S-12, S-20 e pins da 003B.
- `backend/app/main.py` já restringe métodos e cabeçalhos CORS.
- O backend tem apenas rotas `GET /` e `GET /health`; não há integrações HTTP externas em uso.
- As versões globais instaladas e observadas são FastAPI 0.141.1, Pydantic 2.13.5 e Uvicorn 0.52.4; a `.venv` existente está em Python 3.12 e usa pins antigos.
- Upload de fotos deve continuar fora da API, por envio direto ao storage, conforme `docs/PLANO-MESTRE.md`.

## Critérios de aceite
- [x] Limitar o corpo de requisições HTTP a 1 MiB, sem confiar apenas no cabeçalho `Content-Length` e sem acumular corpos ilimitados em memória.
- [x] Responder `413` com mensagem genérica para corpos acima do limite; manter os endpoints e seus contratos atuais.
- [x] Sanitizar erros de validação: não incluir valores submetidos, contexto interno nem dados sensíveis na resposta.
- [x] Responder a erros inesperados com `500` genérico, sem stack trace ou mensagem da exceção no corpo HTTP.
- [x] Testar limites, validação sanitizada, erro interno genérico e manutenção dos headers de segurança.
- [x] Confirmar que não existem chamadas HTTP externas no backend atual; registrar que timeouts serão obrigatórios ao introduzir cada integração externa, sem adicionar cliente ou dependência sem uso nesta tarefa.
- [x] Atualizar somente os pins de runtime necessários para alinhar FastAPI, Pydantic e Uvicorn às versões globais observadas: `fastapi==0.141.1`, `pydantic==2.13.5`, `uvicorn[standard]==0.52.4`.
- [x] Validar instalação e testes com Python 3.12; executar `ruff check app tests`, `mypy app` e `pytest`.
- [x] Atualizar o estado da tarefa 003 na seção 18 de `docs/PLANO-MESTRE.md` e preencher o relatório do executor.

## Arquivos que podem ser alterados
- `backend/app/**`
- `backend/tests/**`
- `backend/requirements.txt`
- `docs/PLANO-MESTRE.md` (seção 18 e estado da base, se necessário)
- `docs/tasks/003B-hardening-restante.md`
- `docs/reviews/003B-hardening-restante.md`

## Fora de escopo
- Alterar rotas ou contratos de negócio existentes.
- Criar login, autorização, upload, pagamento ou qualquer integração externa.
- Alterar frontend, MCPs, skills, agentes ou configuração OpenCode.
- Atualizar dependências de desenvolvimento ou adicionar novas dependências.
- Subir banco ou outros serviços Docker.
- Repetir reorganizações de frontend/raiz já cobertas na tarefa 003.

## Regras de segurança aplicáveis
- Aplicar S-12 e S-20 do plano mestre.
- Não incluir dados submetidos, segredos, detalhes de exceção ou stack traces em respostas HTTP.
- Não ler arquivos `.env` nem alterar arquivos com credenciais.
- Preservar CORS restrito e os headers de segurança existentes.
- Não usar `--auto`.

## Como testar
1. `backend/.venv` com Python 3.12 e pins de runtime atualizados.
2. `ruff check app tests`.
3. `mypy app`.
4. `pytest`.
5. Confirmar respostas 413/422/500 sanitizadas e headers de segurança nos testes.
6. `git diff --check` e revisar que o escopo não incluiu frontend nem regras de negócio.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito: adicionado limite de corpo de 1 MiB com contagem dos chunks recebidos (sem confiar em `Content-Length`); respostas genéricas para 413, 422 e 500; headers de segurança mantidos também nos erros; pins de FastAPI, Pydantic e Uvicorn atualizados. Nenhuma chamada HTTP externa existe no backend; configurar timeouts ao adicionar cada integração externa.
- Arquivos alterados: `backend/app/main.py`, `backend/app/core/errors.py`, `backend/app/middleware/body_limit.py`, `backend/tests/test_health.py`, `backend/tests/test_hardening.py`, `backend/requirements.txt`, `docs/PLANO-MESTRE.md`, `docs/tasks/003B-hardening-restante.md`, `docs/reviews/003B-hardening-restante.md`.
- Validação: Python 3.12.7; FastAPI 0.141.1, Pydantic 2.13.5 e Uvicorn 0.52.4 instalados na `.venv`; `ruff check app tests` e `mypy app` aprovados; `pytest` com 8 testes aprovados.
- Dúvidas ou riscos: `pytest` emite um aviso de depreciação do `TestClient`/Starlette devido à dependência HTTPX existente; sem impacto nos testes e sem nova dependência adicionada.
