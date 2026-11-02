# Revisão 003C - Agentes, skills, MCPs e permissões

## Resultado
Não aprovado: a configuração atual não satisfaz os critérios de aceite. A revisão anterior afirmava que alguns valores estavam configurados, mas eles não aparecem no `opencode.json` atual.

## Critérios de aceite
- [x] 5 skills movidas para `.opencode/skills/<nome>/SKILL.md`; diretórios e nomes do frontmatter conferem.
- [ ] `mcp.shadcn-ui.enabled` e `mcp.chrome-devtools.enabled` em `false`: **falhou**; ambos estão `true` em `opencode.json:18-28`.
- [ ] `permission.skill` com `"*": "ask"`: **falhou**; ausente da configuração do projeto.
- [ ] `.env` e `.env.*` em `deny`, com `*.env.example` liberado por regra final: **falhou**; a exceção não consta e o bloqueio local `.env.*` prevalece.
- [ ] `build` restrito: **falhou**; a saída de `opencode agent list` mostra permissão efetiva ampla `* allow`, sem as negações de comando requeridas.
- [ ] `plan`, `explore` e `general` com `edit: deny`: **parcial**; a execução atual herda negações globais, mas a configuração do projeto não as declara como exigido.
- [ ] `security-reviewer` criado como `mode: subagent`: **parcial**; o agente está carregado e bloqueia edição/bash, mas está definido como `mode: all`.
- [x] `CLAUDE.md` contém seção "Agentes".
- [ ] Validações de MCP e execução real dos agentes repetidas com a configuração atual.

## Validações do revisor
| Comando | Resultado |
|---|---|
| Inspeção de `.opencode/skills/` | 5 diretórios; `SKILL.md` e nome do frontmatter correspondem |
| `opencode agent list` (auditoria atual) | Configuração carregada; `security-reviewer (all)` presente; `build` mostra `* allow` herdado |
| `opencode mcp list` | Não executado: MCPs habilitados usam `npx -y`; evitar download/execução antes da correção e aprovação |
| Inspeção de `opencode.json` | MCPs habilitados; ausência de `permission.skill`, regras de build e exceção `*.env.example` |
| Execução de skills/agentes via prompt | Não repetida nesta auditoria; validação registrada anteriormente não confirma a configuração atual |

## Observações
- Como `security-reviewer` tem `bash: deny`, ele não executa `git diff` sozinho; o coordenador deve enviar o diff no pedido.
- `permission.skill` em `ask` pode bloquear o carregamento de skills em execuções não interativas (`opencode run`). Tarefas que exigirem skill devem ser conduzidas de forma interativa ou listar a skill com antecedência.
- As cópias globais em `~/.config/opencode/skills/*.md` continuam no formato antigo e não são carregadas; fora do escopo do repositório.
- Remoto Git configurado em `https://github.com/FagnerDSantos/pics.git`; `master` com upstream.
- O MCP oficial de shadcn é o comando `shadcn@latest mcp`; `shadcn-ui-mcp-server` é comunitário. Chrome DevTools publica o pacote `chrome-devtools-mcp` oficialmente.

## Ajustes necessários
- Corrigir `opencode.json` de acordo com os critérios restantes, sem habilitar os MCPs por padrão.
- Revalidar com a configuração corrigida; só então aprovar a tarefa.
