# Retomada do trabalho

Atualizado em 2026-11-01. Este arquivo é o checkpoint curto do projeto; leia-o antes de retomar, junto com `CLAUDE.md` e `docs/PLANO-MESTRE.md`. Atualize-o ao concluir ou pausar uma tarefa. Não precisa guardar o histórico inteiro do chat.

## Último ponto confirmado

- Projeto: `C:\desenvolvimento\pics`, branch `master`.
- Tarefa 003B (hardening restante) concluída e validada; commit `6ac5929 fix: conclui hardening restante do backend`.
- Validações 003B: Python 3.12.7; FastAPI 0.141.1, Pydantic 2.13.5 e Uvicorn 0.52.4; `ruff check app tests`, `mypy app`, `pytest` (8 passaram) e `git diff --check` aprovados. O pytest mostrou um aviso não bloqueante de depreciação do TestClient/Starlette.
- Próxima frente: auditoria/correção da tarefa 003C (agentes, skills, MCPs e permissões), antes de iniciar a tarefa 004.

## Auditoria OpenCode em andamento

- Há cinco skills em `.opencode/skills/<nome>/SKILL.md`; os nomes do frontmatter correspondem às pastas e todas têm descrição. A estrutura é carregável, mas as descrições não dizem claramente quando ativar cada skill e o conteúdo ainda precisa de revisão de qualidade. Ainda não foi repetido um teste de ativação de skill nesta retomada.
- `opencode agent list` executou e lista `build`, `plan`, `explore`, `general` e `security-reviewer`; o último está em `mode: all`, com `edit: deny` e `bash: deny`.
- A configuração efetiva não corresponde ao relatório anterior da 003C: `opencode.json` deixa `shadcn-ui` e `chrome-devtools` com `enabled: true`, não define `permission.skill`, não contém os bloqueios Bash planejados para `build` e não explicita as permissões `edit: deny` para `plan`, `explore` e `general` no escopo do projeto. A regra local de leitura também não libera `*.env.example` após o bloqueio de `.env.*`.
- Não executar `opencode mcp list` nem iniciar esses MCPs enquanto estiverem habilitados: os comandos configurados usam `npx -y`, que pode baixar/executar pacotes. Primeiro confirmar os pacotes oficiais e deixar os MCPs desligados por padrão, conforme as regras do projeto.
- O agente `security-reviewer` cobre somente requisitos S-xx e requer que o diff seja fornecido no prompt. Não há agente revisor geral de mudanças. Recomenda-se uma tarefa para um `change-reviewer` somente leitura, separado do agente que implementa; ainda não foi criado.

## Alterações locais preservadas

Após o commit 003B, permanecem no working tree alterações pendentes da 003C e de configuração local: renomes staged das cinco skills; mudanças em `CLAUDE.md`, `opencode.json` e `docs/tasks/003C-agentes-skills-mcps.md`; `.opencode/agent/security-reviewer.md`; arquivos do plugin local de fallback de modelo; `docs/reviews/003C-agentes-skills-mcps.md` e `opencode.json.pre-go-fallback.bak`. Não incluir esses arquivos em commits da 003B nem descartá-los sem revisão explícita.

## Próximos passos

1. Criar uma tarefa de correção/auditoria 003C com os problemas acima e alinhar `docs/tasks/003C-agentes-skills-mcps.md` e sua revisão com a configuração real.
2. Com aprovação, corrigir permissões e MCPs; validar o JSON e a lista de agentes; validar skills com prompt fictício; somente testar servidores MCP após confirmar os pacotes e manter dados fictícios.
3. Propor e aprovar a criação do agente de revisão geral. O coordenador deve continuar executando testes/lint e fornecer o diff ao agente revisor; agente revisor não edita nem executa comandos.
