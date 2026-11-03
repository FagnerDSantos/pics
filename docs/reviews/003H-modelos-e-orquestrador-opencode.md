# Revisão 003H — Modelos e orquestrador OpenCode

## Resultado

**Aprovado.** A configuração e o prompt mantêm os papéis aprovados e os modelos selecionados por Fagner. O orquestrador é o agente padrão, coordena sem editar nem executar Bash e delega somente aos agentes autorizados. `build` permanece o executor único; DBA e revisores continuam consultivos/somente leitura.

## Critérios revisados

| Critério | Resultado | Evidência |
|---|---|---|
| Orchestrator padrão, primary, sem edição/Bash | Aprovado | `opencode debug config` e `opencode debug agent orchestrator`; asserts de permissões |
| Delegação allowlist | Aprovado | Wildcard e `general` negados; somente `explore`, `plan`, `postgres-dba`, `build`, `change-reviewer` e `security-reviewer` permitidos |
| Fluxo e limites no prompt | Aprovado | `prompts/orchestrator.md` exige leitura inicial de `CLAUDE.md`, `docs/PLANO-MESTRE.md` e `docs/RETOMADA.md`; descreve sequência, aprovações e limites |
| Modelos dos sete agentes | Aprovado | `opencode debug agent` resolveu cada ID esperado |
| Papéis/permissões preservados | Aprovado | DBA e revisores continuam sem read/edit/bash/task conforme configuração; build continua executor; explore/plan mantêm restrições existentes |
| Configurações restantes preservadas | Aprovado | `small_model`, regras de leitura, bloqueios Git e MCPs desativados foram conferidos |
| Smoke tests funcionais do orquestrador | Aprovado | Invocações padrão sem `--agent` chamaram `explore` → `plan`, `postgres-dba` e `security-reviewer` com fixtures sintéticas e modelos escolhidos; nenhuma edição, Bash ou web |
| Documentação da tarefa/checkpoint | Aprovado | Atualizados `docs/tasks/003H-modelos-e-orquestrador-opencode.md` e `docs/RETOMADA.md` |

## Validações executadas

- `opencode models opencode-go --verbose`: todos os modelos escolhidos constavam como ativos; o catálogo mostra custo não nulo. Fagner aprovou as chamadas sujeitas a cobrança antes dos smoke tests.
- `opencode debug config` e `opencode debug agent <nome>`: default e sete modelos efetivos corretos.
- Assertions PowerShell: permissões do orquestrador, allowlist, permissões de DBA/revisores e executor build passaram.
- `opencode run --pure --agent orchestrator --format json` e, depois, `opencode run --pure --format json` (agente padrão): delegação sintética `explore` → `plan` concluída. A segunda invocação confirmou a resolução do agente padrão, com dependência fictícia `B → A`; nenhum dado do produto foi passado aos subagentes.
- Outras invocações padrão via `opencode run --pure --format json`: uma encaminhou proposta fictícia de remover `studio_id` ao `postgres-dba` (modelo `minimax-m3`), que recomendou bloquear a migration; outra enviou diff SQL fictício ao `security-reviewer` (modelo `qwen3.8-max`), que identificou risco alto S-27. Ambas usaram apenas contexto sintético e não acionaram ferramentas de edição ou shell.
- `change-reviewer` revisou a configuração da tarefa usando `deepseek-v4-pro`; `build` aplicou a correção do prompt com `kimi-k2.7-code`. Os testes de configuração confirmaram também os modelos de `orchestrator`, `explore` e `plan`.
- `git diff --check`: passou; foram emitidos apenas avisos de conversão LF/CRLF em alguns arquivos modificados.
- Lint/testes do produto: não aplicáveis; a tarefa alterou apenas configuração e documentação OpenCode.

## Achados do change-reviewer e resolução

- Primeira revisão: achado baixo em `prompts/orchestrator.md` por não exigir leitura inicial de `docs/RETOMADA.md`. Corrigido na linha 3; a revisão final confirmou o atendimento.
- Revisão final: critérios funcionais aprovados; pendência bloqueante restrita à ausência de relatório e atualização do checkpoint na evidência fornecida. Este relatório e o checkpoint foram então criados/atualizados, atendendo ao critério documental.
- A primeira execução longa de `build` atingiu timeout de 300 segundos sem resposta final. O log indicou alterações e assertions; o coordenador repetiu as verificações de configuração e permissões independentemente. Uma chamada curta posterior de `build` aplicou a correção da revisão e terminou normalmente.
- Não foram criados scripts temporários no repositório; as verificações foram comandos inline. Alterações preexistentes foram preservadas. Nenhum commit/push foi feito.

## Próximo passo

O `orchestrator` já está definido como padrão no projeto. Reinicie ou abra uma nova sessão OpenCode para que clientes/TUIs já abertos recarreguem a configuração; então use o fluxo normal, sempre com tarefa aprovada e dados fictícios quando necessário.
