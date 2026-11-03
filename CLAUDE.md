# CLAUDE.md — Pics (plataforma SaaS para fotógrafos)

Dono do produto e decisor final: **Fagner**. Responda e escreva docs e commits em pt-BR. Código e identificadores em inglês.

## O que é
SaaS multi-tenant: cada fotógrafo é um **estúdio** (tenant). Ordem de entrega, definida pelo Fagner:
**B1 Entrega de fotos → B2 Álbuns → B3 Gestão do estúdio e site.**
Status vivo: `docs/RETOMADA.md`. Escopo e regras: `docs/PLANO-MESTRE.md`.
**Ferramenta única: Claude Code.** O OpenCode foi descontinuado. `AGENTS.md`, `opencode.json`, `.opencode/` e `prompts/` não são fonte de regra; não os use nem edite (remoção em D-31).

## Leia sob demanda (economiza tokens)
- **Não leia o plano inteiro.** Ele é grande. Use o mapa de leitura (§0.2) e as seções que a tarefa listar em "Ler:".
- Para achar uma seção: `grep -n "^## " docs/PLANO-MESTRE.md` e leia só o intervalo de linhas.
- Pedidos específicos (arquivo, função, critério de aceite) em vez de "explore o projeto".

## Stack
- Backend (`backend/`): Python 3.12/3.13 em venv, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, PostgreSQL.
- Frontend (`frontend/`): Next 16 (App Router), TypeScript estrito, Tailwind.
- Infra local (`infra/`): Docker Compose (PostgreSQL, MinIO, Mailpit).
- Checks (iguais ao CI `.github/workflows/ci.yml`): em `backend/`, com a `.venv` ativa: `ruff check app tests`, `mypy app`, `pytest` (testes de banco pedem `DATABASE_URL` sintético e PostgreSQL de teste no Docker). Em `frontend/`: `npm run lint`, `npm run typecheck`, `npm run build`. Sempre: `git diff --check`.
- Ambiente: Windows 11, Docker Desktop com WSL 2. Use PowerShell ou Git Bash conforme o comando.

## Regras inegociáveis
1. **Multi-tenant:** toda tabela de negócio tem `studio_id`; toda consulta filtra por estúdio; RLS no banco; storage em `studios/{studio_id}/...`. Rota nova ou alterada exige teste de isolamento entre dois estúdios. Fluxos sem estúdio conhecido (link do cliente, webhook, login) só resolvem o estúdio pelas funções da §8 regra 8 do plano; nunca com `BYPASSRLS`.
2. **Dinheiro** em centavos (inteiro). **Datas** em UTC. **UI** em pt-BR.
3. **Pagamento** só é confirmado por webhook assinado e idempotente. Nunca por ação do cliente. Estorno ou MED recalcula o estado financeiro e revoga links de entrega.
4. **Original** nunca chega ao navegador antes de a matriz de liberação (plano §4.3) permitir. A decisão é do servidor, em `services/release.py`.
5. **Segredos:** nunca ler nem escrever `.env`, por nenhuma ferramenta (Read, Grep, Bash, PowerShell: `cat`, `type`, `Get-Content`, `printenv`, `env`). O bloqueio de `.claude/settings.json` cobre só as ferramentas de arquivo; o resto depende de você. Sem chaves, fotos reais ou dados de clientes em prompts, logs, testes ou commits. Use dados fictícios.
6. **Uma tarefa por vez.** O que estiver fora do escopo vira observação em `docs/reviews/`, sem correção por conta própria.
7. **git commit** antes e depois de cada tarefa, só com os arquivos da tarefa (nunca `git add -A`). `git push` só com pedido do Fagner. No máximo 2 rodadas de correção; depois pare e consulte.
8. Nunca usar `--dangerously-skip-permissions` nem modo de aprovação automática.
9. Skills e MCPs: só os que a tarefa listar.

## REQUER APROVAÇÃO do Fagner (pare e pergunte)
Dependência nova (confira que o nome é o oficial) · mudança de arquitetura ou ADR · migração destrutiva · mudança no esquema multi-tenant · provedor de Pix, storage ou e-mail · textos jurídicos/LGPD · shadcn/ui · instalação global · **uso do Opus**.

## Fluxo por tarefa
1. Sessão nova (`/clear`). Leia a tarefa `docs/tasks/NNN-nome.md` e só as seções do plano que ela lista.
2. Se a tarefa tocar mais de 3 arquivos, esquema, auth, pagamento ou storage: plano antes (Shift+Tab, modo plan) e mostre ao Fagner.
3. Implemente em passos pequenos. Rode os checks do passo, não do projeto inteiro, quando possível.
4. Revisão por subagentes (contexto limpo): `change-reviewer` sempre; `postgres-dba` se tocar esquema, migração, RLS ou função `SECURITY DEFINER`; `security-reviewer` se tocar auth, pagamento, estorno, storage, download, link de cliente ou rota nova. Passe a eles o número da tarefa; eles leem o diff sozinhos.
5. Pronto = DoD do plano §15: checks verdes, testes de isolamento e da matriz quando couber, relatório em `docs/reviews/NNN-nome.md`, `docs/RETOMADA.md` atualizado, commit feito.

## Modelos e tokens (detalhes na skill `economia-de-tokens`)
- **Sonnet** é o padrão (planejar tarefas normais, implementar, testar, revisar).
- **Haiku** para busca, leitura, resumo de log, commit message e tarefas mecânicas (use o subagente `Explore`).
- **Opus só em último caso e só para planejar algo complexo**, com aprovação do Fagner. Nunca para escrever código rotineiro nem revisar.
- Esforço padrão `medium` (`/effort`). Não defina `CLAUDE_CODE_EFFORT_LEVEL` em settings: ele sobrepõe o `/effort`. Teto de gasto com IA: US$ 50/mês (D-30); meça com `/usage`.
- Dê `/clear` entre tarefas e ao mudar de assunto. Saída volumosa (testes, logs, buscas largas) vai para subagente.
- Quando perceber sinal de que convém `/clear`, `/compact` ou trocar de modelo, diga em uma linha e prepare 3 a 5 linhas de resumo para a sessão nova. Quem digita o comando é o Fagner.

# Compact instructions

Ao compactar, preserve: número e critérios de aceite da tarefa, arquivos alterados, decisões tomadas, saída de testes que falharam, itens aguardando aprovação do Fagner e o próximo passo.
