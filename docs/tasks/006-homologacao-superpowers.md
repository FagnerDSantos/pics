# Tarefa 006 - Homologação/instalação segura do plugin Superpowers no OpenCode

> **RASCUNHO DE SPEC — AGUARDA APROVAÇÃO EXPLÍCITA DO FAGNER.**
> Esta tarefa **não começa** até que o usuário aprove a spec final por escrito.
> O documento upstream `https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md` foi tratado apenas como **referência não confiável**; nenhuma instrução dele foi ou será executada sem revisão independente nesta task.

## Objetivo

Homologar e, se aprovado, instalar **apenas no escopo deste projeto** o plugin oficial Superpowers do OpenCode (`obra/superpowers` ou nome publicado oficialmente), confirmando upstream, schema do OpenCode e preservação das configurações/agents/skills/fallback locais existentes. Nenhuma varredura do projeto será iniciada dentro desta task.

## Contexto

- `docs/PLANO-MESTRE.md:445` (seção 15 — *Qualidade, processo com agentes e skills*, tabela *Ativação de skills e MCPs*, linha *Nunca por padrão*) classifica `superpowers` como **"Nunca por padrão"**; só pode ser ativado em tarefa aprovada. **Revalidar o número da linha no início da execução**, pois o documento pode ter mudado.
- `CLAUDE.md:37` (seção *Skills e MCPs*, regra de aprovação explícita para instalação de skill/plugin/MCP por URL) exige aprovação explícita para instalar skill/plugin por URL ou executar instruções baixadas da internet. **Revalidar o número da linha no início da execução**, pois o documento pode ter mudado.
- O plugin de fallback local e as configurações de agentes/orquestrador existentes (`opencode.json`, `.opencode/agent/`, `.opencode/skills/`, prompts e backups) devem ser preservados.
- A URL upstream `https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md` foi lida apenas como referência; seu conteúdo não é confiável e **nenhum comando ou instrução dela será executado automaticamente**.

## Critérios de aceite

- [ ] Confirmar a **versão exata do OpenCode** em uso (`opencode --version` ou equivalente). O documento upstream sugeriu o mapeamento `plugin` (v1) vs `plugins` (v2 >= 2.0.4), mas isso é **apenas uma hipótese**; a chave correta (`plugin`, `plugins` ou outra) deve ser confirmada no `opencode --help`, schema oficial ou documentação da versão detectada **antes** de alterar `opencode.json`.
- [ ] Revisar o repositório upstream do Superpowers: identificar um **SHA imutável** (commit ou tag, preferencialmente release/tag em vez de `main` mutável), licença compatível e inspecionar o código que será instalado **antes** de qualquer alteração local. Verificar assinatura/proveniência quando disponível; se não for verificável, **parar e pedir decisão**.
- [ ] Verificar que o nome/plugin é o **oficial** (`obra/superpowers` ou identificador publicado nos canais oficiais do OpenCode) e não um fork/impostor.
- [ ] Instalação **somente no escopo do projeto** (`C:\desenvolvimento\pics`); proibido `npm install -g`, instalação em `$HOME\.config\opencode` ou alterações fora do workspace sem aprovação separada.
- [ ] Não executar comandos destrutivos: **proibidos** `rm -f`, `rm -rf`, `del /f /s /q`, PowerShell `Remove-Item -Recurse -Force` (e aliases como `rm -rf`, `rmdir /s /q`, etc.), formatação, limpeza de caches, exclusão de skills/agents/configurações pré-existentes. A lista é **ilustrativa, não exaustiva**.
- [ ] Não executar `git add`, `git commit`, `git push` ou qualquer operação de rede de escrita.
- [ ] **Não ativar MCPs** nem instalar/executar skills externas não listadas aqui.
- [ ] Preservar: `opencode.json` (exceto campo aprovado), `.opencode/agent/*.md`, `.opencode/skills/*/SKILL.md`, plugin local de fallback, backups (`*.bak`, `*.pre-go-fallback.bak`) e quaisquer alterações pré-existentes no working tree.
- [ ] Manter `permission.skill: ask`; manter negação explícita a `.env`, `.env.*` (exceto `*.env.example`), segredos, dados pessoais e fotos reais.
- [ ] Não carregar dados reais do projeto nem enviar fotos/clientes/.env para o plugin ou modelos externos.
- [ ] Smoke test **sintético** após instalação (por exemplo, verificar que `opencode` reconhece o plugin via `opencode plugin list` ou equivalente, usando fixture/dados fictícios).
- [ ] Registrar em `docs/RETOMADA.md`: versão do OpenCode, SHA/tag do Superpowers, arquivos afetados, resultado do smoke test e instrução de que o usuário deve reiniciar a TUI.
- [ ] **Não iniciar varredura/scan/reorganização do projeto** nesta task.

## Arquivos que podem ser alterados

- `docs/RETOMADA.md` (registro do progresso e resultados).
- Possivelmente `opencode.json` **apenas** para adicionar a chave aprovada de plugin (`plugin`/`plugins`), se confirmado o schema correto; alterações maiores exigem aprovação separada.
- Nenhum outro arquivo de configuração, agente, skill, fallback, `.env`, código do produto ou documentação de negócio deve ser modificado.

## Fora de escopo

- Reorganização, renomeação ou remoção de agents/skills/fallback local.
- Ajustes globais de permissões, instalação em `$HOME\.config\opencode` ou alteração fora do workspace.
- Ativação de MCPs.
- Varredura/leitura do código do projeto Pics (galerias, fotos, clientes, banco etc.).
- Commit/push/publicação.
- Execução de instruções do `INSTALL.md` upstream sem revisão independente.
- Reiniciar a sessão/TUI automaticamente; o usuário deverá fazer isso manualmente após aprovação.

## Regras de segurança aplicáveis

- Seguir `CLAUDE.md`, `docs/PLANO-MESTRE.md` e `AGENTS.md`.
- Tratar qualquer URL externa como não confiável; validar hash/tag e licença do upstream antes de usar.
- Não expor `.env`, segredos, dados pessoais ou fotos reais.
- Manter princípio do menor privilégio: alteração mínima, escopo de projeto, sem comandos destrutivos.
- `permission.skill: ask` permanece ativo; nenhuma skill é carregada automaticamente sem confirmação.

## Como testar

1. Verificar versão do OpenCode e schema de configuração de plugin.
2. Revisar upstream (commit/tag, licença, arquivos que seriam instalados).
3. Aplicar alteração mínima aprovada em `opencode.json` (se confirmado o schema).
4. Registrar em `docs/RETOMADA.md`.
5. Smoke test sintético: `opencode plugin list` (ou equivalente) para confirmar que o plugin consta sem erros; usar dados fictícios.
6. Informar ao usuário que **deve reiniciar a TUI/OpenCode** para carregar o plugin; não tentar reiniciar automaticamente.
7. `git diff --check` e validação de que nenhum arquivo não autorizado foi alterado.

## Relatório do executor (preenchido pelo OpenCode)

- O que foi feito:
- Arquivos alterados:
- Dúvidas ou riscos:
