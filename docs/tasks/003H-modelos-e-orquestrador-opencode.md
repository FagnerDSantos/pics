# Tarefa 003H - Modelos por agente e orquestrador OpenCode

## Objetivo
Ativar o `orchestrator` como agente padrão do projeto e atribuir aos agentes existentes os modelos escolhidos por Fagner, preservando papéis, permissões e o fluxo definido em `CLAUDE.md`.

## Contexto
- `opencode.json` atualmente define `build` como agente primário implícito e configura modelos diferentes dos escolhidos agora.
- `postgres-dba`, `change-reviewer` e `security-reviewer` têm modelo definido no frontmatter de seus arquivos em `.opencode/agent/`.
- Fagner confirmou que `postgres-dba` permanece consultivo/somente leitura, `build` permanece o único executor de código e os dois revisores continuam separados.
- A proposta inicial de DBA com edição/Bash e os agentes `implementer`/`frontend` com escrita foram descartados.
- `opencode models opencode-go --verbose` listou os modelos selecionados como ativos; o catálogo exibe valores de uso não nulos para eles. Chamadas funcionais podem gerar cobrança conforme a conta/provedor.

## Critérios de aceite
- [x] Definir `default_agent` como `orchestrator`, configurado como `primary`, sem permissão de editar arquivos ou executar Bash.
- [x] Criar o prompt do orquestrador com o fluxo compatível com `CLAUDE.md`: explorar, planejar quando necessário, consultar `postgres-dba` antes de mudanças de banco, delegar implementação somente a `build`, revisar com `change-reviewer` e usar `security-reviewer` separadamente quando aplicável.
- [x] Permitir ao orquestrador delegar somente a `explore`, `plan`, `postgres-dba`, `build`, `change-reviewer` e `security-reviewer`; negar outros destinos, inclusive `general`.
- [x] Configurar os modelos exatos escolhidos por Fagner:
  - `orchestrator`: `opencode-go/gpt-6-luna`
  - `explore`: `opencode-go/deepseek-v4.1-flash`
  - `plan`: `opencode-go/kimi-k3.1-pro`
  - `postgres-dba`: `opencode-go/minimax-m3`
  - `build`: `opencode-go/kimi-k2.7-code`
  - `change-reviewer`: `opencode-go/deepseek-v4-pro`
  - `security-reviewer`: `opencode-go/qwen3.8-max`
- [x] Preservar as permissões efetivas dos agentes existentes: `build` como executor; DBA, revisores e agentes de exploração/planejamento sem escrita fora do que já lhes foi autorizado; revisores sem Bash/task.
- [x] Preservar as demais configurações existentes em `opencode.json`, incluindo `small_model`, regras de leitura, proteção contra comandos Git destrutivos e MCPs desativados.
- [x] Validar o JSON e a configuração carregada com o CLI; confirmar nomes, modo, modelos e permissões efetivas dos agentes.
- [x] Após aprovação explícita do custo, fazer smoke tests do orquestrador usando apenas contexto e instruções sintéticas, sem dados reais, segredos ou `.env`, e confirmar pelo resultado que ele delegou a agentes permitidos sem editar arquivos.
- [x] Atualizar `docs/RETOMADA.md` e criar `docs/reviews/003H-modelos-e-orquestrador-opencode.md` com resultados reais.

## Arquivos que podem ser alterados
- `opencode.json`
- `.opencode/agent/postgres-dba.md` (somente campo de modelo, se necessário)
- `.opencode/agent/change-reviewer.md` (somente campo de modelo, se necessário)
- `.opencode/agent/security-reviewer.md` (somente campo de modelo, se necessário)
- `prompts/orchestrator.md`
- `docs/tasks/003H-modelos-e-orquestrador-opencode.md`
- `docs/reviews/003H-modelos-e-orquestrador-opencode.md`
- `docs/RETOMADA.md`

## Fora de escopo
- Alterar papéis, permissões de escrita ou o processo de execução/revisão já aprovado.
- Criar os agentes `implementer`, `frontend` ou um segundo revisor geral.
- Dar escrita, Bash, leitura de arquivos ou delegação ao `postgres-dba`.
- Alterar plugins, ativar MCPs, instalar dependências ou skills.
- Alterar código do produto, banco de dados ou migrações.
- Enviar código do projeto, dados pessoais, fotos, segredos ou `.env` a modelos durante o smoke test.

## Regras de segurança aplicáveis
- `orchestrator` apenas coordena; edição e Bash permanecem negados.
- `postgres-dba` permanece consultivo e somente leitura; `build` implementa models e migrations após consulta ao DBA e aprovação aplicável.
- `change-reviewer` e `security-reviewer` mantêm escopos separados e somente leitura.
- Usar apenas fixtures sintéticas no smoke test; interromper se a delegação tentar incluir conteúdo local do repositório.
- Os modelos listados têm preços de uso não nulos no catálogo. Não enviar prompts funcionais até Fagner confirmar a execução sujeita a esses custos.
- Não usar `--auto`, não instalar nada e não ligar MCPs.

## Como testar
1. Validar a sintaxe JSON de `opencode.json`.
2. Executar `opencode agent list` e confirmar o agente padrão/orquestrador, modelos selecionados e permissões dos agentes.
3. Fazer smoke test sintético do orquestrador somente após aprovação explícita de uso/custo; verificar a delegação e a ausência de edição/comandos.
4. Executar `git diff --check` e revisar o diff limitado aos arquivos autorizados.

## Aprovação
Fagner confirmou a direção, aprovou os modelos e o uso do orquestrador e respondeu “Sim” à execução da tarefa e aos custos de chamadas aos modelos.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito: `orchestrator` passou a ser o agente padrão, sem `edit`/Bash e com delegação allowlist; os sete modelos foram atribuídos conforme aprovado. O prompt foi ajustado na primeira revisão para exigir leitura inicial de `CLAUDE.md`, `docs/PLANO-MESTRE.md` e `docs/RETOMADA.md`.
- Arquivos alterados nesta tarefa: `opencode.json`; `.opencode/agent/postgres-dba.md`, `.opencode/agent/change-reviewer.md` e `.opencode/agent/security-reviewer.md` (somente modelo); `prompts/orchestrator.md`; este arquivo; `docs/reviews/003H-modelos-e-orquestrador-opencode.md`; `docs/RETOMADA.md`.
- Validações reais: catálogo OpenCode listou modelos ativos; `opencode debug config`/`opencode debug agent` confirmaram IDs, default e permissões; asserts PowerShell passaram; smoke tests sintéticos pelo agente padrão confirmaram delegação para `explore` → `plan`, `postgres-dba` e `security-reviewer`, cada um com somente dados fictícios; `build` também respondeu à correção pontual usando o modelo selecionado. `git diff --check` passou com avisos LF/CRLF. Nenhum teste de produto era aplicável.
- Revisão: change-reviewer aprovou os critérios funcionais; o achado inicial baixo sobre leitura da retomada foi corrigido. A revisão final pediu que este relatório e o checkpoint fossem registrados; ambos foram atualizados.
- Dúvidas ou riscos: a primeira execução extensa de `build` foi encerrada pelo timeout do terminal após 300 segundos, sem resposta final; validações de configuração foram repetidas pelo coordenador e passaram, e uma invocação curta posterior do `build` aplicou a correção revisada. Nenhum commit/push foi feito; havia alterações locais preexistentes não relacionadas que foram preservadas. O smoke test utilizou somente dados sintéticos.
