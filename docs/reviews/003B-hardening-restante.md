# Revisão 003B - Hardening restante e atualização de pins

## Resultado
Implementação aprovada após revisão e validações locais.

## Critérios de aceite
- [x] Limite de corpo de 1 MiB aplicado por contagem do corpo recebido, independentemente de `Content-Length`.
- [x] Corpos acima do limite recebem 413 genérico e a resposta mantém os headers de segurança.
- [x] Erros de validação retornam mensagem genérica sem refletir os valores enviados.
- [x] Erros inesperados retornam 500 genérico sem detalhes da exceção ou stack trace.
- [x] Testes cobrem limites, sanitização de 422/500 e headers de segurança.
- [x] Nenhuma chamada HTTP externa encontrada no backend; timeouts ficam como requisito para cada futura integração.
- [x] Pins de runtime alinhados: FastAPI 0.141.1, Pydantic 2.13.5 e Uvicorn 0.52.4.
- [x] Validações executadas com Python 3.12.7.

## Validações
| Comando | Resultado |
|---|---|
| `ruff check app tests` | Aprovado |
| `mypy app` | Aprovado (13 arquivos fonte) |
| `pytest` | 8 aprovados; 1 aviso de depreciação do TestClient/Starlette |
| `git diff --check` | Aprovado para o diff rastreado; arquivos novos revisados também |

## Arquivos revisados
- `backend/app/main.py`
- `backend/app/core/errors.py`
- `backend/app/middleware/body_limit.py`
- `backend/tests/test_health.py`
- `backend/tests/test_hardening.py`
- `backend/requirements.txt`
- `docs/tasks/003B-hardening-restante.md`
- `docs/PLANO-MESTRE.md`

## Ajustes necessários
Nenhum bloqueante identificado. O aviso de depreciação do TestClient/Starlette não afeta os testes e não foi adicionada dependência fora do escopo.
