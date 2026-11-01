# Tarefa 003C - Agentes, skills, MCPs e permissões

## Objetivo
Alinhar a configuração do OpenCode às regras do `CLAUDE.md` e do plano mestre: corrigir o formato das skills, desligar MCPs por padrão, restringir permissões perigosas e criar o agente `security-reviewer` somente leitura com modelo de outra família.

## Contexto
Diagnóstico atual: 5 skills em `.opencode/skills/*.md` não são carregadas (o formato exigido é `.opencode/skills/<nome>/SKILL.md`); `shadcn-ui` e `chrome-devtools` estão `enabled: true` (`opencode.json:22,27`) contrariando `CLAUDE.md:36`; todos os agentes herdam permissões amplas; não existe revisor de segurança (S-26). O `gh` não está instalado, então o remoto Git fica fora desta tarefa.

## Critérios de aceite
- [ ] Mover as 5 skills para `.opencode/skills/<nome>/SKILL.md` via `git mv`, mantendo o frontmatter e o nome igual ao da pasta: `agent-superpowers`, `cloudflare-security-audit`, `gsap-animation-guidelines`, `lgpd-brazil-compliance`, `vercel-web-interface-guidelines`.
- [ ] Em `opencode.json`, definir `mcp.shadcn-ui.enabled = false` e `mcp.chrome-devtools.enabled = false`.
- [ ] Em `opencode.json`, adicionar `permission.skill` com `"*": "ask"` para exigir aprovação ao carregar skill.
- [ ] Em `opencode.json`, ajustar `permission.read` para manter `.env` e `.env.*` em `deny`, mas permitir explicitamente `*.env.example` (regra de exceção por último).
- [ ] Em `opencode.json`, restringir o agente `build`: `edit: allow`, e em `bash` manter `"*": "allow"` com regras finais `git push*: deny`, `git commit*: deny`, `git reset --hard*: deny`, `git clean*: deny` e `Remove-Item*: ask`.
- [ ] Em `opencode.json`, garantir `permission.edit: deny` para `plan`, `explore` e `general`.
- [ ] Criar `.opencode/agent/security-reviewer.md` (`mode: subagent`, `model: opencode/glm-5.3-flash-free`, `temperature: 0.1`) com `edit: deny` e `bash: deny`; o prompt deve instruir revisão somente leitura de `git diff` contra os itens S-xx do plano mestre, apontando riscos e referenciando `arquivo:linha`, sem alterar código.
- [ ] Atualizar `CLAUDE.md` com uma seção curta "Agentes" listando `build`, `plan`, `explore`, `security-reviewer` e quando usar cada um.
- [ ] Validações: `opencode agent list` mostra `security-reviewer`; `opencode mcp list` mostra os dois MCPs desligados; `opencode run --agent build "Responda apenas OK"` inicia sem erro de configuração; `Get-ChildItem .opencode/skills/*/SKILL.md` retorna 5 arquivos.

## Arquivos que podem ser alterados
- `.opencode/skills/**`
- `.opencode/agent/security-reviewer.md`
- `opencode.json`
- `CLAUDE.md`

## Fora de escopo
- Configurar Git remoto (bloqueado: `gh` não instalado).
- Alterar a configuração global em `~/.config/opencode/`.
- Instalar dependências, plugins ou novos MCPs.
- Tarefas 003B, 004 e 005.
- Alterar código de `backend/` ou `frontend/`.

## Regras de segurança aplicáveis
- Nenhum segredo, chave ou token em `opencode.json` ou no agente.
- MCPs desligados por padrão; só ligar na tarefa que os citar.
- `security-reviewer` não pode editar arquivos nem executar comandos.
- Não ativar skill sem aprovação (`permission.skill` em `ask`).

## Como testar
1. `Get-ChildItem .opencode/skills/*/SKILL.md` → 5 arquivos.
2. `opencode agent list` → `security-reviewer (subagent)` presente.
3. `opencode mcp list` → `shadcn-ui` e `chrome-devtools` desligados.
4. `opencode run --agent build "Responda apenas OK"` → executa sem erro de config.
5. `git status` → apenas os arquivos permitidos alterados.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito:
- Arquivos alterados:
- Dúvidas ou riscos:
