# Retomada do trabalho

Atualizado em 2026-11-01. Este arquivo é o checkpoint curto do projeto; leia-o antes de retomar, junto com `CLAUDE.md` e `docs/PLANO-MESTRE.md`. Atualize-o ao concluir ou pausar uma tarefa. Não precisa guardar o histórico inteiro do chat.

## Último ponto confirmado

- Tarefa 004 implementada, com validação final do Compose pendente: pacote `pics-frontend` e lockfile para as dependências declaradas; typecheck e headers de segurança; Compose local para PostgreSQL, MinIO e Mailpit; CI com `npm ci`, lint, typecheck, build, auditoria npm com limiar alto/crítico e Gitleaks; Dependabot, hook Gitleaks, seis ADRs em proposta e README atualizado. `.editorconfig` e `.gitignore` existentes já cobriam o escopo.
- A tela 004A não foi alterada. Smoke check em `http://127.0.0.1:3000` respondeu HTTP 200, `lang=pt-BR` e cabeçalhos CSP, Referrer-Policy e Permissions-Policy.
- Validações 004: `npm ci`, `npm run lint`, `npm run typecheck`, `npm run build`, `ruff check app tests`, `mypy app`, `pytest` (8 passaram), `npm audit --audit-level=high`, análise YAML do Compose com PyYAML e `git diff --check` passaram. `npm audit` completo encontrou 16 vulnerabilidades moderadas em dependências de desenvolvimento; `npm audit --omit=dev` encontrou zero e `npm audit fix --dry-run` não ofereceu correção compatível. Nenhuma dependência foi atualizada. Fagner aprovou o limiar de CI alto/crítico. `docker compose config` bloqueado porque Docker CLI não está instalado; nenhum container foi iniciado ou baixado.
- Após autorização para pausar, a prévia foi reiniciada em `http://127.0.0.1:3000`; smoke check respondeu HTTP 200, `lang=pt-BR` e headers de segurança.
- Configuração Docker solicitada: ambiente bloqueado porque Docker Desktop/CLI e WSL não estão instalados, a sessão não é administradora e o firmware informa virtualização desativada. Diagnóstico e procedimento em `docs/tasks/004B-configurar-docker-local.md` e `docs/reviews/004B-configurar-docker-local.md`; nada foi instalado nem iniciado.
- O ambiente bloqueia `git commit`; nenhum `git add` ou `git commit` foi executado. Relatório da tarefa: `docs/reviews/004-frontend-e-raiz.md`.
- Fagner solicitou publicar o projeto no Git. Verificação: branch `master` está 8 commits à frente de `origin/master`, com alterações locais ainda não commitadas. Esta sessão não conseguiu executar commit/push por restrição da ferramenta; o fallback OpenCode e seu backup seguem preservados e não devem ser publicados sem revisão explícita do risco registrado abaixo.
- Tarefa 004A (`docs/tasks/004A-tela-demonstrativa.md`) concluída: prévia responsiva em pt-BR, com indicadores fictícios e sem ações conectadas. `frontend/src/app/layout.tsx` contém idioma e metadados descritivos; a página ganhou atalho de teclado ao conteúdo principal e ajustes de contraste/foco. Revisão registrada em `docs/reviews/004A-tela-demonstrativa.md`.
- Prévia local disponível em `http://127.0.0.1:3000`; smoke check HTTP 200 confirmou HTML, idioma e conteúdo demonstrativo. Inspeção visual em viewports ainda não realizada.
- Arquivos desta tarefa: `frontend/src/app/page.tsx`, `frontend/src/app/globals.css`, `frontend/src/app/layout.tsx`, `docs/tasks/004A-tela-demonstrativa.md`, `docs/reviews/004A-tela-demonstrativa.md` e este checkpoint. Alterações locais OpenCode foram preservadas.
- Validações da tarefa 004A: `npm run lint`, `npm run build` e `git diff --check` aprovados. Lint/build emitiram apenas o aviso do npm sobre `msvs_version` em configuração local.
- O ambiente bloqueia `git commit`; nenhum commit foi criado para esta tarefa.
- Projeto: `C:\desenvolvimento\pics`, branch `master`.
- Tarefa 003B (hardening restante) concluída e validada; commit `6ac5929 fix: conclui hardening restante do backend`.
- Este mecanismo de checkpoint foi registrado no commit `a8ffb50 docs: adiciona checkpoint de retomada`.
- Validações 003B: Python 3.12.7; FastAPI 0.141.1, Pydantic 2.13.5 e Uvicorn 0.52.4; `ruff check app tests`, `mypy app`, `pytest` (8 passaram) e `git diff --check` aprovados. O pytest mostrou um aviso não bloqueante de depreciação do TestClient/Starlette.
- Tarefa 003C corrigida e validada no commit `7956c51 fix: endurece configuração dos agentes OpenCode`.
- Tarefa 003D (`docs/tasks/003D-change-reviewer.md`) preparada e registrada; o agente ainda não foi implementado. A implementação fica para tarefa separada após aprovação.

## Avaliação da estrutura

- A base de monorepo está organizada para continuar a fundação, mas não está pronta para produção: backend ainda tem somente rotas básicas e não tem banco/migrações/autenticação; frontend permanece uma prévia demonstrativa; o Compose, CI, lockfile e documentação base da tarefa 004 estão preparados. A auditoria npm reportou vulnerabilidades moderadas transitivas; tratar em tarefa autorizada de dependências.

## Auditoria OpenCode em andamento

- Há cinco skills em `.opencode/skills/<nome>/SKILL.md`; os nomes do frontmatter correspondem às pastas. `opencode run --agent plan` listou as cinco skills locais. As descrições continuam sem gatilhos claros de ativação e a qualidade do conteúdo merece tarefa futura.
- `opencode agent list` executou e lista `build`, `plan`, `explore`, `general` e `security-reviewer`; o último está em `mode: subagent`, com `edit: deny` e `bash: deny`.
- A configuração corrigida tem `permission.skill: ask`; `.env`/`.env.*` negados com exceção `*.env.example`; regras explícitas para build/plan/explore/general; leitura ampla da pasta global do OpenCode removida; ambos os MCPs desativados.
- A origem dos comandos foi pesquisada sem instalá-los: MCP oficial do shadcn pelo CLI `shadcn` (`npx shadcn@latest mcp`); `chrome-devtools-mcp` oficial, com `--no-usage-statistics`. `opencode mcp list` confirma os dois desligados; não foi iniciada conexão com os servidores.
- O agente `security-reviewer` cobre somente requisitos S-xx e requer que o diff seja fornecido no prompt. Não há agente revisor geral de mudanças. Recomenda-se uma tarefa para um `change-reviewer` somente leitura, separado do agente que implementa; ainda não foi criado.
- O plugin local de fallback de modelos passou em `node --test .opencode/model-fallback.test.mjs` (4 testes), com aviso de `MODULE_TYPELESS_PACKAGE_JSON`. Há risco de privacidade que ainda precisa de decisão: ele pode reenviar o prompt original a outro provedor/modelo após certos erros; revisar contra a regra de não enviar dados sensíveis a modelos gratuitos antes de adotá-lo.

## Alterações locais preservadas

Os commits 003C e da tarefa preparada 003D estão fechados. Permanecem no working tree, salvos em disco mas sem commit, a escolha de modelos `opencode-go/gpt-6-luna` em `opencode.json`, os arquivos do plugin local de fallback, seu teste e `opencode.json.pre-go-fallback.bak`. Não descartar nem incluir esses arquivos em outro commit sem revisão explícita. O plugin de fallback pode reenviar prompts para outros provedores; decidir se deve ficar ativo antes de usá-lo com dados não fictícios.

## Decisão de escopo

- Fagner aprovou os marcos M0–M6. Roadmap, entregáveis, critérios, dependências, gates de decisão e status inicial estão registrados na seção 14 e 18 de `docs/PLANO-MESTRE.md`; revisão em `docs/reviews/003E-marcos-entrega.md`.
- Capacidade informada: 25 horas por semana (a mensagem mais recente corrige a estimativa anterior de 40 horas).
- Previsão de planejamento, sujeita a revisões: M0–M2 (prévia de fotos, acesso do cliente, seleção e expiração) até 20/12/2026, com margem até 10/01/2027; fluxo completo M0–M4 (álbum, Pix e originais após pagamento) até 15/02/2027, com margem até 28/02/2027. Pressupõe escopo estável e decisões/aprovações sem longos bloqueios.

## Próximos passos

1. Retomar publicação em uma sessão com permissão para `git commit`/`git push`; revisar explicitamente se os arquivos locais do fallback devem ser excluídos ou publicados.
2. Habilitar AMD SVM/AMD-V no firmware e disponibilizar sessão Windows administrativa; então instalar/configurar WSL 2 e Docker Desktop, validar `docker compose config`, concluir 004 e executar 005.
3. Aprovar a execução da tarefa 003D antes de criar o agente `change-reviewer`, se desejado.
4. Reiniciar o cliente OpenCode para carregar a configuração 003C; o processo/sessão atual não pode reiniciar a si próprio com segurança.
