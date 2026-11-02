# Revisão 003C - Agentes, skills, MCPs e permissões

## Resultado
Aprovado após corrigir as divergências encontradas na auditoria.

## Critérios de aceite
- [x] 5 skills movidas para `.opencode/skills/<nome>/SKILL.md`; diretórios e nomes do frontmatter conferem.
- [x] `mcp.shadcn-ui.enabled` e `mcp.chrome-devtools.enabled` em `false`; shadcn usa o CLI oficial e Chrome DevTools tem estatísticas desativadas.
- [x] `permission.skill` com `"*": "ask"`.
- [x] `.env` e `.env.*` em `deny`, com `*.env.example` liberado por regra final; removida a permissão ampla para ler `~/.config/opencode/`.
- [x] `build` restrito: comandos de alteração remota/destrutiva em `deny` e `Remove-Item*` em `ask`.
- [x] `plan`, `explore` e `general` com `edit: deny` no escopo do projeto.
- [x] `security-reviewer` criado como `mode: subagent`, modelo `glm-5.3-flash-free`, `edit: deny`, `bash: deny`, `task: deny`.
- [x] `CLAUDE.md` contém seção "Agentes".
- [x] Validações de configuração e execução sintética repetidas com a configuração corrigida.

## Validações do revisor
| Comando | Resultado |
|---|---|
| Inspeção de `.opencode/skills/` | 5 diretórios; `SKILL.md` e nome do frontmatter correspondem |
| `opencode agent list` | Configuração válida; `security-reviewer (subagent)` com `edit`, `bash` e `task` em `deny`; permissões de `build`, `plan`, `explore` e `general` presentes |
| `opencode mcp list` | `shadcn-ui` e `chrome-devtools` aparecem como `disabled`; nenhum processo MCP iniciado |
| `Get-ChildItem .opencode/skills/*/SKILL.md` | 5 arquivos |
| `opencode run --agent build "Responda apenas OK"` | `OK`, modelo gratuito, prompt sintético, plugins desativados |
| `opencode run --agent plan "Liste somente os nomes das skills..."` | Listou as cinco skills locais e a skill interna `customize-opencode` |
| `node -e ... JSON.parse(opencode.json)` | JSON válido após remover BOM UTF-8 para validação |

## Observações
- Como `security-reviewer` tem `bash: deny`, ele não executa `git diff` sozinho; o coordenador deve enviar o diff no pedido.
- `permission.skill` em `ask` pode bloquear o carregamento de skills em execuções não interativas (`opencode run`). Tarefas que exigirem skill devem ser conduzidas de forma interativa ou listar a skill com antecedência.
- As cópias globais em `~/.config/opencode/skills/*.md` continuam no formato antigo e não são carregadas; fora do escopo do repositório.
- Remoto Git configurado em `https://github.com/FagnerDSantos/pics.git`; `master` com upstream.
- Os MCPs permanecem desligados por padrão. A conectividade dos servidores não foi testada, pois a política do projeto manda ativá-los somente quando uma tarefa os exigir.

## Ajustes necessários
Nenhum bloqueante para a 003C. A avaliação de conteúdo/qualidade das descrições das skills permanece fora do escopo desta tarefa.
