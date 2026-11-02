# Retomada do trabalho

Atualizado em 2026-11-01. Este arquivo é o checkpoint curto do projeto; leia-o antes de retomar, junto com `CLAUDE.md` e `docs/PLANO-MESTRE.md`. Atualize-o ao concluir ou pausar uma tarefa. Não precisa guardar o histórico inteiro do chat.

## Último ponto confirmado

- Projeto: `C:\desenvolvimento\pics`, branch `master`.
- Tarefa 003B (hardening restante) concluída e validada; commit `6ac5929 fix: conclui hardening restante do backend`.
- Este mecanismo de checkpoint foi registrado no commit `a8ffb50 docs: adiciona checkpoint de retomada`.
- Validações 003B: Python 3.12.7; FastAPI 0.141.1, Pydantic 2.13.5 e Uvicorn 0.52.4; `ruff check app tests`, `mypy app`, `pytest` (8 passaram) e `git diff --check` aprovados. O pytest mostrou um aviso não bloqueante de depreciação do TestClient/Starlette.
- Tarefa 003C corrigida e validada nesta sessão; commit de fechamento pendente. A tarefa 003D (agente revisor geral) foi preparada; execução é etapa separada.

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

Para o commit da 003C estão staged somente os arquivos da tarefa: renomes de skills, agente revisor de segurança, `CLAUDE.md`, `opencode.json`, plano e documentos de tarefa/revisão. Permanecem fora desse commit o modelo escolhido anteriormente no `opencode.json` (será restaurado como mudança não staged após o commit), o plugin local de fallback de modelo, `docs/tasks/003D-change-reviewer.md` e o backup `opencode.json.pre-go-fallback.bak`.

## Próximos passos

1. Fechar a 003C em commit isolado e restaurar a alteração preexistente de modelo, mantendo-a fora do commit da tarefa.
2. Commitar a tarefa preparada `docs/tasks/003D-change-reviewer.md` separadamente; sua execução fica para aprovação/tarefa posterior.
3. Após a conversa de escopo, atualizar o plano mestre apenas com a decisão acordada.
