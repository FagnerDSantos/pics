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

Os commits 003C e da tarefa preparada 003D estão fechados. Permanecem no working tree, salvos em disco mas sem commit, a escolha de modelos `opencode-go/gpt-6-luna` em `opencode.json`, os arquivos do plugin local de fallback, seu teste e `opencode.json.pre-go-fallback.bak`. Não descartar nem incluir esses arquivos em outro commit sem revisão explícita. O plugin de fallback pode reenviar prompts para outros provedores; decidir se deve ficar ativo antes de usá-lo com dados não fictícios.

## Decisão de escopo

- Fagner concordou em organizar o trabalho em marcos de entrega no monorepo. A decomposição e os critérios de conclusão de cada marco ainda precisam ser discutidos; o plano mestre do produto não foi reestruturado nesta sessão.

## Próximos passos

1. Definir blocos, entregáveis e critérios de conclusão; atualizar o plano mestre após essa decisão.
2. Aprovar a execução da tarefa 003D antes de criar o agente `change-reviewer`.
3. Decidir se o plugin local de fallback pode permanecer ativo, considerando que reenvia prompts a outros provedores.
4. Reiniciar o cliente OpenCode para carregar a configuração 003C; o processo/sessão atual não pode reiniciar a si próprio com segurança.
