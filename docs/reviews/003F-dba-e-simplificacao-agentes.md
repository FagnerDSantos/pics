# Revisão 003F - Agente DBA e simplificação dos agentes

## Resultado

**Revisão final, aprovação formal, aceitação do critério funcional e commit permanecem pendentes.** A configuração do DBA, a skill local e a simplificação de `general` foram implementadas e suas permissões foram confirmadas pelo CLI durante a execução original. O critério do teste funcional estava inicialmente bloqueado nesta sessão porque a ferramenta de subagent disponível rejeitou o tipo `postgres-dba`.

Há **evidência posterior disponível para avaliação** na tarefa **003H**: o orquestrador encaminhou ao `postgres-dba` uma proposta sintética de remover `studio_id`; o DBA recomendou bloquear a migração, sem editar arquivos, sem usar Bash e sem acessar dados reais. **Esta evidência não é considerada critério já aprovado por esta revisão; a aceitação formal da suficiência dessa evidência indireta aguarda decisão do usuário.** **O teste funcional não foi repetido nesta execução.** Não se declara DoD, publicação ou tarefa formal concluídos.

## Critérios e validações

| Verificação | Resultado |
|---|---|
| Inventário de agentes | `opencode agent list` confirmou os agentes personalizados e integrados; `general` continua integrado ao CLI, sem configuração específica no projeto. `.opencode/agent/` contém os revisores preservados e `postgres-dba`. |
| Simplificação de `general` | `opencode.json` não contém `agent.general`; `permission.task.general` está em `deny`. A tentativa de excluir o built-in do CLI não foi feita. |
| Agente DBA | \`postgres-dba (subagent)\` foi listado com \`read\`, \`edit\`, \`bash\`, \`task\` e \`skill\` em \`deny\`. O modelo originalmente registrado (\`opencode/glm-5.3-flash-free\`) foi substituído pelo alinhamento atual em \`opencode.json\`/\`.opencode/agent/postgres-dba.md\`; esta reconciliação documental não reabre a decisão de modelo nem altera a configuração. **Ressalva:** a configuração atual do \`postgres-dba\` não é afirmada como gratuita; o alinhamento ocorreu por decisão autorizada do usuário. |
| Prompt e skill | Conteúdo inspecionado: análise somente dos insumos fornecidos, limites de dados, foco multi-tenant, RLS, privilégios, SQLAlchemy/Alembic, migrações, consultas/índices, transações e backup/restauração. Nenhum conteúdo externo foi usado. |
| Fluxo em `CLAUDE.md` | Define a consulta ao DBA para mudanças no banco e a decisão do coordenador antes de solicitar correções ao `build`; documenta os usos dos agentes preservados e a distinção do built-in `general`. |
| Configuração JSON | `ConvertFrom-Json` passou; checagens confirmaram ausência de `agent.general` e `permission.task.general=deny`. |
| Teste funcional com fixture textual | **Evidência disponível para avaliação; não aprovada nesta revisão; não repetido agora.** Na execução original desta tarefa, `functions.task` com `subagent_type: postgres-dba` retornou `Unknown agent type: postgres-dba is not a valid agent type`. Posteriormente, em `docs/reviews/003H-modelos-e-orquestrador-opencode.md`, o orquestrador encaminhou ao `postgres-dba` uma proposta sintética de remover `studio_id`; o DBA recomendou bloquear a migração, sem editar, sem Bash e sem dados reais. A suficiência dessa evidência indireta **aguarda aceitação formal do usuário**. |
| `git diff --check` | Passou. O Git informou avisos de conversão LF/CRLF em arquivos modificados. |
| Escopo e preservação | Arquivos alterados por esta tarefa estão na lista permitida. Alterações pré-existentes não relacionadas foram mantidas; não houve `git add`, commit ou push. |

## Observação do coordenador

A inspeção estática e a listagem de permissões não substituem o teste funcional solicitado. O teste funcional solicitado **não foi repetido nesta execução**; há apenas evidência indireta disponível na tarefa 003H, por meio do orquestrador, que deve ser avaliada pelo usuário. **Revisão final, aprovação formal, aceitação do critério funcional, commit e publicação da 003F permanecem pendentes; o DoD não é declarado concluído.**

## Próximo passo

1. **Aprovação humana explícita** da reconciliação documental da 003F e da suficiência da evidência indireta proveniente da 003H para aceitar o critério funcional do `postgres-dba`.
2. **Decidir** se a 003F será considerada concluída sem novo teste funcional repetido agora, ou se será exigida uma nova invocação direta do `postgres-dba` após reinício do runtime.
3. **Reinício/verificação runtime manual do usuário** (não executar automaticamente): abrir uma nova sessão OpenCode para recarregar a configuração atual e confirmar que `postgres-dba` é listado corretamente.
4. **`git add`/`commit`/`push` da 003F somente após aprovação explícita** e com escopo isolado das preexistências do working tree. Não declarar a tarefa formalmente concluída antes disso.
