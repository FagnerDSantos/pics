# Tarefa 003C - Agentes, skills, MCPs e permissões

## Objetivo
Alinhar a configuração do OpenCode às regras do `CLAUDE.md` e do plano mestre: corrigir o formato das skills, desligar MCPs por padrão, restringir permissões perigosas e criar o agente `security-reviewer` somente leitura com modelo de outra família.

## Contexto
Diagnóstico inicial: 5 skills em `.opencode/skills/*.md` não eram carregadas (o formato exigido é `.opencode/skills/<nome>/SKILL.md`); `shadcn-ui` e `chrome-devtools` estavam `enabled: true` contrariando `CLAUDE.md:36`; os agentes herdavam permissões amplas; não existia revisor de segurança (S-26). O `gh` não está instalado, então o remoto Git fica fora desta tarefa.

## Critérios de aceite
- [x] Mover as 5 skills para `.opencode/skills/<nome>/SKILL.md` via `git mv`, mantendo o frontmatter e o nome igual ao da pasta: `agent-superpowers`, `cloudflare-security-audit`, `gsap-animation-guidelines`, `lgpd-brazil-compliance`, `vercel-web-interface-guidelines`.
- [x] Em `opencode.json`, definir `mcp.shadcn-ui.enabled = false` e `mcp.chrome-devtools.enabled = false`; usar o CLI oficial `shadcn` e desativar estatísticas do Chrome DevTools.
- [x] Em `opencode.json`, adicionar `permission.skill` com `"*": "ask"` para exigir aprovação ao carregar skill.
- [x] Em `opencode.json`, ajustar `permission.read` para manter `.env` e `.env.*` em `deny`, permitir explicitamente `*.env.example` (regra de exceção por último) e não abrir leitura ampla da configuração global do OpenCode.
- [x] Em `opencode.json`, restringir o agente `build`: `edit: allow`, e em `bash` manter `"*": "allow"` com regras finais `git push*: deny`, `git commit*: deny`, `git reset --hard*: deny`, `git clean*: deny` e `Remove-Item*: ask`.
- [x] Em `opencode.json`, garantir `permission.edit: deny` para `plan`, `explore` e `general`.
- [x] Criar `.opencode/agent/security-reviewer.md` (`mode: subagent`, `model: opencode/glm-5.3-flash-free`, `temperature: 0.1`) com `edit: deny`, `bash: deny` e `task: deny`; o prompt instrui revisão somente leitura dos itens S-xx com referências `arquivo:linha`.
- [x] Atualizar `CLAUDE.md` com uma seção curta "Agentes" listando `build`, `plan`, `explore`, `security-reviewer` e quando usar cada um.
- [x] Validar `opencode agent list`, `opencode mcp list`, execução sintética de `build` e cinco arquivos `SKILL.md`.

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
5. Revisar `git status` e confirmar que o commit inclui somente os arquivos da 003C, preservando alterações preexistentes fora da tarefa.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito: skills movidas e carregadas; configuração ajustada com MCPs desligados por padrão; permissões de build, leitura, skills e agentes explicitadas; leitura ampla de `~/.config/opencode/` removida; `security-reviewer` em modo `subagent` sem edição, Bash ou delegação; seção de agentes documentada em `CLAUDE.md`.
- Arquivos alterados: cinco `.opencode/skills/*/SKILL.md`, `.opencode/agent/security-reviewer.md`, `opencode.json`, `CLAUDE.md`, `docs/tasks/003C-agentes-skills-mcps.md`, `docs/reviews/003C-agentes-skills-mcps.md`, `docs/PLANO-MESTRE.md`.
- Validações: `opencode agent list` carregou `security-reviewer (subagent)` e mostrou as regras específicas do `build`; `opencode mcp list` mostrou os dois servidores desligados; `opencode run --agent build "Responda apenas OK"` respondeu `OK` usando modelo gratuito com prompt fictício e `OPENCODE_PURE=1` para não executar plugins locais pendentes; `Get-ChildItem .opencode/skills/*/SKILL.md` listou 5 arquivos; `opencode run --agent plan` listou as 5 skills do projeto.
- Dúvidas ou riscos: a conectividade real dos MCPs não foi testada porque devem permanecer desligados por padrão; o Chrome DevTools só deve ser ativado em tarefa que o exija. A escolha de `shadcn@latest mcp` segue a documentação oficial e ainda não instala nem inicia o pacote.
