# Retomada do trabalho

Atualizado em 2026-11-02. Este arquivo é o checkpoint curto do projeto; leia-o antes de retomar, junto com `CLAUDE.md` e `docs/PLANO-MESTRE.md`. Atualize-o ao concluir ou pausar uma tarefa. Não precisa guardar o histórico inteiro do chat.

## Último ponto confirmado

- Tarefa 004 concluída e aprovada: pacote `pics-frontend` e lockfile para as dependências declaradas; typecheck e headers de segurança; Compose local para PostgreSQL, MinIO e Mailpit; CI com `npm ci`, lint, typecheck, build, auditoria npm com limiar alto/crítico e Gitleaks; Dependabot, hook Gitleaks, seis ADRs em proposta e README atualizado. `.editorconfig` e `.gitignore` existentes já cobriam o escopo.
- A tela 004A não foi alterada. Smoke check em `http://127.0.0.1:3000` respondeu HTTP 200, `lang=pt-BR` e cabeçalhos CSP, Referrer-Policy e Permissions-Policy.
- Validações 004: `npm ci`, `npm run lint`, `npm run typecheck`, `npm run build`, `ruff check app tests`, `mypy app`, `pytest` (8 passaram), `npm audit --audit-level=high` e `git diff --check` passaram. `docker compose --env-file .env.example -f infra/docker-compose.yml config` também passou. `npm audit` completo encontrou 16 vulnerabilidades moderadas em dependências de desenvolvimento; `npm audit --omit=dev` encontrou zero e `npm audit fix --dry-run` não ofereceu correção compatível. Nenhuma dependência foi atualizada. Fagner aprovou o limiar de CI alto/crítico.
- Após autorização para pausar, a prévia foi reiniciada em `http://127.0.0.1:3000`; smoke check respondeu HTTP 200, `lang=pt-BR` e headers de segurança.
- Tarefa 004B concluída: Docker Desktop iniciado e operacional com backend WSL2 (`docker-desktop`, versão 2); `docker info` e Compose passaram. Nenhuma imagem foi baixada ou container iniciado. Evidências em `docs/tasks/004B-configurar-docker-local.md` e `docs/reviews/004B-configurar-docker-local.md`.
- Validações deste avanço: `docker --version`, `docker compose version`, `docker info`, `wsl --list --verbose`, `docker compose --env-file .env.example -f infra/docker-compose.yml config` e `git diff --check` executaram; engine está ativo em WSL2, Compose válido e sem imagens/containers.
- Publicação concluída: commit `3aea2c8 chore: publica progresso da fundacao Pics` enviado para `origin/master`; branches sincronizadas. Relatório da tarefa: `docs/reviews/004-frontend-e-raiz.md`.
- Tarefa 005 concluída e validada localmente: migração incremental `backend/alembic/versions/0002_audit_log_append_only.py` rejeita `UPDATE`/`DELETE` em `audit_log`; testes PostgreSQL confirmaram SQLSTATE `55000` e limpeza por reset de schema, sem `DELETE` direto da tabela. O job backend do CI configura PostgreSQL e `DATABASE_URL` sintéticos. Relatório em `docs/reviews/005-postgresql-sqlalchemy-alembic.md`; pytest de integração passou (9 testes, com aviso de depreciação do `TestClient`/Starlette). O PostgreSQL de teste `pics-task005` foi iniciado para os testes e removido com `docker compose down -v`; o estado atual não tem containers nem volumes. `backend/.env.example` usa `postgresql+psycopg://`, compatível com o driver instalado. `ruff check app tests`, `mypy app` e `git diff --check` passaram no ambiente virtual do backend. Publicação preparada em 2026-11-02: arquivos da 005, `docs/PLANO-MESTRE.md` e este checkpoint estão em stage; commit e push devem ser concluídos manualmente porque a sessão atual não tem permissão para executar `git commit`/`git push`.
- Antes desta revisão, o working tree continha a configuração local `opencode.json`, os arquivos do plugin de fallback e seu backup; todos foram preservados e não foram incluídos nas alterações da tarefa 005. O plugin ainda requer revisão explícita do risco de reenvio de prompts.
- Tarefa 004A (`docs/tasks/004A-tela-demonstrativa.md`) concluída: prévia responsiva em pt-BR, com indicadores fictícios e sem ações conectadas. `frontend/src/app/layout.tsx` contém idioma e metadados descritivos; a página ganhou atalho de teclado ao conteúdo principal e ajustes de contraste/foco. Revisão registrada em `docs/reviews/004A-tela-demonstrativa.md`.
- Prévia local disponível em `http://127.0.0.1:3000`; smoke check HTTP 200 confirmou HTML, idioma e conteúdo demonstrativo. Inspeção visual em viewports ainda não realizada.
- Arquivos desta tarefa: `frontend/src/app/page.tsx`, `frontend/src/app/globals.css`, `frontend/src/app/layout.tsx`, `docs/tasks/004A-tela-demonstrativa.md`, `docs/reviews/004A-tela-demonstrativa.md` e este checkpoint. Alterações locais OpenCode foram preservadas.
- Validações da tarefa 004A: `npm run lint`, `npm run build` e `git diff --check` aprovados. Lint/build emitiram apenas o aviso do npm sobre `msvs_version` em configuração local.
- As alterações da tarefa 004A também estão incluídas no commit publicado `3aea2c8`.
- Projeto: `C:\desenvolvimento\pics`, branch `master`.
- Tarefa 003B (hardening restante) concluída e validada; commit `6ac5929 fix: conclui hardening restante do backend`.
- Este mecanismo de checkpoint foi registrado no commit `a8ffb50 docs: adiciona checkpoint de retomada`.
- Validações 003B: Python 3.12.7; FastAPI 0.141.1, Pydantic 2.13.5 e Uvicorn 0.52.4; `ruff check app tests`, `mypy app`, `pytest` (8 passaram) e `git diff --check` aprovados. O pytest mostrou um aviso não bloqueante de depreciação do TestClient/Starlette.
- Tarefa 003C corrigida e validada no commit `7956c51 fix: endurece configuração dos agentes OpenCode`.
- Execução da tarefa 003D aprovada por Fagner e parcialmente realizada: `.opencode/agent/change-reviewer.md` criado com modelo gratuito GLM, `edit`/`bash`/`task`/`skill` negados; `CLAUDE.md` atualizado para incluir revisão independente e impedir que `build` inicie recursivamente outra instância. Relatório em `docs/reviews/003D-change-reviewer.md`.
- Validações 003D: `opencode agent list | Select-String "change-reviewer"` confirmou `change-reviewer (subagent)`; `git diff --check` passou (com avisos de conversão LF/CRLF). O teste funcional ainda está bloqueado: execução direta faz fallback para o agente padrão, e invocações pelo `build` não retornaram em 300 segundos. A tarefa não está aprovada; nenhum commit foi feito.
- Tarefa 003F (`docs/tasks/003F-dba-e-simplificacao-agentes.md`) foi preparada e depois autorizada para execução em 2026-11-02; implementação parcial e bloqueio funcional registrados abaixo.
- Atualização 003F autorizada e implementada parcialmente em 2026-11-02: removida a configuração de projeto `agent.general`, negada delegação para esse alvo, criado `.opencode/agent/postgres-dba.md` (somente leitura) e a skill local `.opencode/skills/postgresql-dba/SKILL.md`; `CLAUDE.md` registra o fluxo de consulta. Arquivos permitidos e resultados em `docs/tasks/003F-dba-e-simplificacao-agentes.md` e `docs/reviews/003F-dba-e-simplificacao-agentes.md`.
- Validações reais 003F: `opencode agent list` mostra `postgres-dba (subagent)` com `read`, `edit`, `bash`, `task` e `skill` negados; `general` continua como agente integrado do CLI, mas `opencode.json` não define `agent.general` e nega `permission.task.general`. `ConvertFrom-Json` e as checagens de configuração passaram; estrutura/conteúdo da skill inspecionados; `git diff --check` passou com avisos LF/CRLF. Nenhuma skill externa ou MCP foi carregado.
- Teste funcional 003F original não concluído: naquela tentativa, `functions.task` respondeu `Unknown agent type: postgres-dba is not a valid agent type`. Depois, na tarefa 003H, o `postgres-dba` foi invocado com sucesso pelo `orchestrator` do OpenCode e analisou uma migration fictícia sem editar ou executar comandos. O registro/revisão próprios da 003F ainda precisam ser reconciliados; não se infere aprovação daquela tarefa.
- As alterações pré-existentes em `CLAUDE.md`, `opencode.json` e nos demais arquivos do working tree foram preservadas; não houve `git add`, commit ou push, conforme instrução da janela.

## Avaliação da estrutura

- A base de monorepo está organizada para continuar a fundação, mas não está pronta para produção: backend ainda tem somente rotas básicas e não tem banco/migrações/autenticação; frontend permanece uma prévia demonstrativa; o Compose, CI, lockfile e documentação base da tarefa 004 estão preparados. A auditoria npm reportou vulnerabilidades moderadas transitivas; tratar em tarefa autorizada de dependências.

## Auditoria OpenCode em andamento

- Há cinco skills em `.opencode/skills/<nome>/SKILL.md`; os nomes do frontmatter correspondem às pastas. `opencode run --agent plan` listou as cinco skills locais. As descrições continuam sem gatilhos claros de ativação e a qualidade do conteúdo merece tarefa futura.
- `opencode agent list` executou e lista `build`, `plan`, `explore`, `general` e `security-reviewer`; o último está em `mode: subagent`, com `edit: deny` e `bash: deny`.
- A configuração corrigida tem `permission.skill: ask`; `.env`/`.env.*` negados com exceção `*.env.example`; regras explícitas para build/plan/explore/general; leitura ampla da pasta global do OpenCode removida; ambos os MCPs desativados.
- A origem dos comandos foi pesquisada sem instalá-los: MCP oficial do shadcn pelo CLI `shadcn` (`npx shadcn@latest mcp`); `chrome-devtools-mcp` oficial, com `--no-usage-statistics`. `opencode mcp list` confirma os dois desligados; não foi iniciada conexão com os servidores.
- O agente `security-reviewer` cobre somente requisitos S-xx e requer que o diff seja fornecido no prompt. `change-reviewer` e `security-reviewer` responderam a fixtures sintéticas; na tarefa 003H, ambos foram usados com os modelos novos e permaneceram somente leitura.
- O plugin local de fallback de modelos passou em `node --test .opencode/model-fallback.test.mjs` (4 testes), com aviso de `MODULE_TYPELESS_PACKAGE_JSON`. Há risco de privacidade que ainda precisa de decisão: ele pode reenviar o prompt original a outro provedor/modelo após certos erros; revisar contra a regra de não enviar dados sensíveis a modelos gratuitos antes de adotá-lo.
- Verificação da hierarquia OpenCode em 2026-11-02: o CLI lista `build`, `plan`, `explore`, `general`, `security-reviewer` e `change-reviewer`, além de agentes internos (`compaction`, `summary`, `title`). `opencode mcp list` confirmou `shadcn-ui` e `chrome-devtools` desligados. `explore` e `general` têm edição negada, mas Bash permitido por herança; os dois revisores têm edição e Bash negados. Não há métrica de uso acumulado disponível.

## Alterações locais preservadas

Os commits 003C e da tarefa preparada 003D estão fechados. Permanecem no working tree, salvos em disco mas sem commit, a escolha de modelos `opencode-go/gpt-6-luna` em `opencode.json`, os arquivos do plugin local de fallback, seu teste e `opencode.json.pre-go-fallback.bak`. Não descartar nem incluir esses arquivos em outro commit sem revisão explícita. O plugin de fallback pode reenviar prompts para outros provedores; decidir se deve ficar ativo antes de usá-lo com dados não fictícios.

## Decisão de escopo

- Fagner aprovou os marcos M0–M6. Roadmap, entregáveis, critérios, dependências, gates de decisão e status inicial estão registrados na seção 14 e 18 de `docs/PLANO-MESTRE.md`; revisão em `docs/reviews/003E-marcos-entrega.md`.
- Capacidade informada: 25 horas por semana (a mensagem mais recente corrige a estimativa anterior de 40 horas).
- Previsão de planejamento, sujeita a revisões: M0–M2 (prévia de fotos, acesso do cliente, seleção e expiração) até 20/12/2026, com margem até 10/01/2027; fluxo completo M0–M4 (álbum, Pix e originais após pagamento) até 15/02/2027, com margem até 28/02/2027. Pressupõe escopo estável e decisões/aprovações sem longos bloqueios.

## Próximos passos

1. Executar/revisar o job backend do GitHub Actions após publicação autorizada das alterações da tarefa 005; CI remoto pendente e nenhum commit foi feito nesta revisão, conforme solicitado.
2. Revisar e decidir se o plugin local de fallback pode permanecer e se suas alterações devem ser publicadas.
3. Reconciliar o relatório/revisão 003D com o uso sintético bem-sucedido do `change-reviewer` via ferramenta suportada e pelo orquestrador; a tentativa histórica `opencode run --agent change-reviewer` ainda fazia fallback.
4. Reiniciar/abrir uma nova sessão OpenCode para carregar a configuração atual do `orchestrator` e os modelos; a sessão atual não pode reiniciar a si própria com segurança.
5. Reconciliar o relatório/revisão 003F com a invocação sintética bem-sucedida do `postgres-dba` pelo orquestrador; a aprovação formal da tarefa 003F continua pendente.

## Validação read-only 003G — 2026-11-02

- Backend: `ruff check app tests`, `mypy app` e `pytest` não executaram. Os comandos não estão no PATH; as tentativas com `py -3.12 -m ...` e `python -m ...` confirmaram que os módulos não estão instalados nas instalações Python 3.12 e 3.14. Nenhuma dependência foi instalada.
- Antes da tentativa de pytest, foi verificado sem imprimir o conteúdo que `DATABASE_URL` está ausente no ambiente do processo. O teste de banco não chegou a executar; contagem de testes executados: 0.
- Frontend: `npm run lint`, `npm run typecheck` e `npm run build` concluíram com sucesso. `npm audit --audit-level=high` não identificou vulnerabilidades altas/críticas; reportou 16 moderadas. Houve aviso npm de configuração local desconhecida `msvs_version`.
- Compose: `docker --version` confirmou Docker 29.9.2; `docker compose --env-file .env.example -f infra/docker-compose.yml config --quiet` validou a configuração sem saída. Nenhum serviço foi iniciado.
- Nenhum banco foi acessado. Arquivos relevantes: `backend/requirements-dev.txt`, `backend/pyproject.toml`, `frontend/package.json`, `infra/docker-compose.yml`.
- Próximo passo: disponibilizar a toolchain já declarada em `backend/requirements-dev.txt` e repetir ruff, mypy e pytest com `DATABASE_URL` ausente.

## Tarefa 003H — modelos e orquestrador OpenCode — 2026-11-02

- Fagner decidiu manter os papéis e permissões atuais, trocar os modelos dos agentes pelos IDs informados e usar um `orchestrator`; o DBA segue consultivo/somente leitura, `build` segue executor único e os dois revisores permanecem separados.
- `opencode models opencode-go --verbose` listou os sete modelos escolhidos como ativos e com preços não nulos; Fagner aprovou chamadas sujeitas a cobrança.
- `opencode.json` define `orchestrator` como padrão, em modo `primary`, sem edição/Bash e com allowlist para `explore`, `plan`, `postgres-dba`, `build`, `change-reviewer` e `security-reviewer`. Os sete modelos resolvidos no CLI correspondem aos selecionados.
- `prompts/orchestrator.md` segue o processo do projeto e exige leitura inicial de `CLAUDE.md`, `docs/PLANO-MESTRE.md` e `docs/RETOMADA.md`; DBA e revisores permanecem somente leitura, e `build` segue executor único.
- Smoke tests funcionais via `opencode run --pure --format json` sem especificar `--agent`: o agente padrão delegou `explore` → `plan` e respeitou a dependência fictícia B → A; em invocações separadas, delegou cenário de migration fictícia ao `postgres-dba` (recomendou bloqueio) e diff SQL fictício ao `security-reviewer` (identificou risco alto S-27). Nenhum arquivo de produto foi editado, nenhum Bash/web foi usado e nenhum dado real ou segredo foi enviado. `change-reviewer` também revisou a tarefa após a configuração, e `build` respondeu à correção pontual usando o modelo selecionado.
- Validações: `opencode debug config`, `opencode debug agent`, assertions de modelos/permissões e `git diff --check` passaram. A primeira execução longa de `build` expirou após 300s sem mensagem final; o coordenador repetiu as validações relevantes, e a chamada curta de correção do prompt retornou com sucesso. Sem testes de produto (não aplicáveis).
- Revisão independente em `docs/reviews/003H-modelos-e-orquestrador-opencode.md`: achado baixo do prompt foi corrigido; a pendência documental apontada na revisão final foi resolvida com este checkpoint e o relatório. Working tree já continha alterações não relacionadas, preservadas; sem commit/push.
- Próximo passo: reiniciar/abrir uma nova sessão OpenCode para clientes/TUIs recarregarem a configuração e usar o `orchestrator` como agente padrão.
