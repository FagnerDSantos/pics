# Retomada do trabalho

Atualizado em 2026-11-01. Este arquivo é o checkpoint curto do projeto; leia-o antes de retomar, junto com `CLAUDE.md` e `docs/PLANO-MESTRE.md`. Atualize-o ao concluir ou pausar uma tarefa. Não precisa guardar o histórico inteiro do chat.

## Último ponto confirmado

- Projeto: `C:\desenvolvimento\pics`, branch `master`.
- Tarefa 003B (hardening restante) concluída e validada; commit `6ac5929 fix: conclui hardening restante do backend`.
- Este mecanismo de checkpoint foi registrado no commit `a8ffb50 docs: adiciona checkpoint de retomada`.
- Validações 003B: Python 3.12.7; FastAPI 0.141.1, Pydantic 2.13.5 e Uvicorn 0.52.4; `ruff check app tests`, `mypy app`, `pytest` (8 passaram) e `git diff --check` aprovados. O pytest mostrou um aviso não bloqueante de depreciação do TestClient/Starlette.
- Tarefa 003C corrigida e validada no commit `7956c51 fix: endurece configuração dos agentes OpenCode`.
- Tarefa 003D (`docs/tasks/003D-change-reviewer.md`) preparada e registrada; o agente ainda não foi implementado. A implementação fica para tarefa separada após aprovação.

## Avaliação da estrutura

- A base de monorepo e backend organizada é adequada para continuar a fase de fundação, mas não está pronta para produção: backend ainda tem somente rotas básicas e não tem banco/migrações/autenticação; frontend ainda é boilerplate; falta `frontend/package-lock.json`; o Compose contém só PostgreSQL, sem MinIO/Mailpit; o CI ainda usa `npm install` e não executa `tsc`, auditoria de dependências ou varredura de segredos. Parte disso está prevista nas tarefas 004–006.

## Auditoria OpenCode em andamento

- Há cinco skills em `.opencode/skills/<nome>/SKILL.md`; os nomes do frontmatter correspondem às pastas. `opencode run --agent plan` listou as cinco skills locais. As descrições continuam sem gatilhos claros de ativação e a qualidade do conteúdo merece tarefa futura.
- `opencode agent list` executou e lista `build`, `plan`, `explore`, `general` e `security-reviewer`; o último está em `mode: subagent`, com `edit: deny` e `bash: deny`.
- A configuração corrigida tem `permission.skill: ask`; `.env`/`.env.*` negados com exceção `*.env.example`; regras explícitas para build/plan/explore/general; leitura ampla da pasta global do OpenCode removida; ambos os MCPs desativados.
- A origem dos comandos foi pesquisada sem instalá-los: MCP oficial do shadcn pelo CLI `shadcn` (`npx shadcn@latest mcp`); `chrome-devtools-mcp` oficial, com `--no-usage-statistics`. `opencode mcp list` confirma os dois desligados; não foi iniciada conexão com os servidores.
- O agente `security-reviewer` cobre somente requisitos S-xx e requer que o diff seja fornecido no prompt. Não há agente revisor geral de mudanças. Recomenda-se uma tarefa para um `change-reviewer` somente leitura, separado do agente que implementa; ainda não foi criado.
- O plugin local de fallback de modelos passou em `node --test .opencode/model-fallback.test.mjs` (4 testes), com aviso de `MODULE_TYPELESS_PACKAGE_JSON`. Há risco de privacidade que ainda precisa de decisão: ele pode reenviar o prompt original a outro provedor/modelo após certos erros; revisar contra a regra de não enviar dados sensíveis a modelos gratuitos antes de adotá-lo.

## Alterações locais preservadas

O commit 003C está fechado. Permanece como alteração local a escolha de modelos `opencode-go/gpt-6-luna` em `opencode.json`, restaurada após o commit e mantida fora dele. Os arquivos do plugin local de fallback, seu teste e `opencode.json.pre-go-fallback.bak` também continuam sem commit; não os descartar nem incluir em outro commit sem revisão explícita. A tarefa 003D e a atualização correspondente do plano/checkpoint estão sendo registradas em commit documental separado.

## Próximos passos

1. Discutir e decidir os blocos do escopo do produto; só então atualizar o plano mestre.
2. Aprovar a execução da tarefa 003D antes de criar o agente `change-reviewer`.
3. Revisar o risco de privacidade e decidir se o plugin local de fallback pode reenviar prompts a outros provedores.
