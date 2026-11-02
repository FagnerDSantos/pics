# Tarefa 004 - Frontend e raiz

## Objetivo
Concluir a fundação do frontend e da raiz do monorepo: dependências frontend reproduzíveis, cabeçalhos de segurança, ambiente local preparado, CI, Dependabot, varredura de segredos, ADRs e instruções atualizadas. Preservar a tela demonstrativa 004A.

## Contexto
- Tarefa do marco M0, aprovada no plano mestre (`docs/PLANO-MESTRE.md`, seção 14).
- O frontend já usa Next.js 16, React 19, TypeScript e Tailwind; a tela provisória está em `frontend/src/app/page.tsx`.
- `infra/docker-compose.yml`, CI, `.gitignore` e `.editorconfig` já existem e devem ser completados, não substituídos sem necessidade.
- O roadmap prevê PostgreSQL, MinIO e Mailpit no Compose; preparar a configuração, sem subir serviços.
- Não adicionar nem atualizar pacotes npm/Python. O lockfile deve corresponder exatamente às dependências já declaradas.

## Critérios de aceite
- [x] Renomear o pacote frontend para `pics-frontend`, versionar `frontend/package-lock.json` e manter as dependências declaradas sem alterações.
- [x] Adicionar script `typecheck`; configurar cabeçalhos de segurança no Next.js, incluindo CSP, HSTS, `nosniff`, `frame-ancestors 'none'`, Referrer-Policy e Permissions-Policy, compatíveis com desenvolvimento local e produção.
- [x] Completar Compose para PostgreSQL, MinIO e Mailpit com portas locais, volumes e credenciais configuráveis por ambiente; documentar `.env.example` sem segredos; não iniciar nem baixar os serviços.
- [x] Atualizar CI para usar `npm ci`, lint, `tsc`, build e `npm audit --audit-level=high`; preservar os checks backend e adicionar varredura de segredos com Gitleaks.
- [x] Adicionar Dependabot para npm, pip e GitHub Actions e hook local de Gitleaks, sem instalar ferramentas ou pacotes.
- [x] Criar ADR-001 a ADR-006 em estado de proposta; nenhuma decisão foi marcada como aprovada.
- [x] Atualizar README com instalação, execução, variáveis de ambiente, serviços locais e comandos de qualidade.
- [x] Confirmar se `.editorconfig` e `.gitignore` existentes cobrem o escopo; alterar somente se faltar regra necessária.
- [x] Preservar a tela e os dados fictícios da tarefa 004A; não alterar a identidade visual provisória além do necessário para compatibilidade técnica.
- [x] `npm ci`, `npm run lint`, `npm run typecheck`, `npm run build` e verificações backend passam.
- [x] `npm audit --audit-level=high` passa e falha para vulnerabilidades de severidade alta ou crítica; os 16 achados moderados em dependências de desenvolvimento permanecem documentados. `npm audit --omit=dev` não encontra vulnerabilidades.
- [ ] `docker compose config` valida a configuração sem subir containers; Docker CLI não está disponível no ambiente. A sintaxe YAML foi verificada com PyYAML.
- [x] Atualizar `docs/RETOMADA.md` e criar `docs/reviews/004-frontend-e-raiz.md`.

## Arquivos que podem ser alterados
- `.editorconfig`
- `.gitignore`
- `.github/workflows/ci.yml`
- `.github/dependabot.yml`
- `.pre-commit-config.yaml`
- `README.md`
- `.env.example`
- `infra/docker-compose.yml`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/next.config.ts`
- `docs/adr/ADR-001-*.md` a `docs/adr/ADR-006-*.md`
- `docs/tasks/004-frontend-e-raiz.md`
- `docs/reviews/004-frontend-e-raiz.md`
- `docs/RETOMADA.md`

## Fora de escopo
- Alterar dependências ou versões npm/Python, instalar ferramentas ou adicionar pacotes.
- Implementar banco, migrações, rotas de produto, login, upload ou processamento de fotos (tarefas 005+).
- Iniciar containers ou conectar serviços externos.
- Aprovar decisões propostas nos ADRs ou decisões pendentes D-01 a D-11.
- Refazer a interface demonstrativa ou definir a identidade visual final (tarefas 020–022).
- Ler ou alterar `.env`, arquivos locais OpenCode ou dados reais.

## Regras de segurança aplicáveis
- Segredos somente em variáveis locais; `.env.example` contém apenas valores fictícios de desenvolvimento.
- Compose deve expor serviços somente em loopback e usar credenciais explicitamente de desenvolvimento, configuráveis pelo `.env`.
- CSP deve reduzir origens e capacidades ao mínimo necessário; qualquer exceção de desenvolvimento deve ser condicionada ao modo de desenvolvimento.
- Gitleaks e CI não devem imprimir conteúdo de segredos.
- Não executar `docker compose up` nem baixar imagens durante a tarefa.

## Como testar
1. Em `frontend/`, executar `npm ci`, `npm run lint`, `npm run typecheck`, `npm run build`, `npm audit` e `npm audit --audit-level=high`.
2. Executar os checks do backend: `ruff check app tests`, `mypy app` e `pytest`.
3. Executar `docker compose -f infra/docker-compose.yml config` sem iniciar serviços.
4. Revisar regras de CI, Dependabot, Gitleaks, headers, lockfile e ADRs.
5. Executar `git diff --check` e revisar que só os arquivos permitidos foram alterados.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito: pacote do frontend renomeado e lockfile gerado sem alterar as dependências declaradas; script TypeScript e cabeçalhos configurados; Compose preparado sem iniciar serviços; CI, Dependabot, Gitleaks, ADRs e README atualizados. `.editorconfig` e `.gitignore` existentes cobrem o escopo. A tela 004A permaneceu intacta e respondeu HTTP 200 com idioma pt-BR e CSP no smoke check local.
- Arquivos alterados: `.env.example`, `.github/dependabot.yml`, `.github/workflows/ci.yml`, `.pre-commit-config.yaml`, `README.md`, `docs/adr/ADR-001` a `ADR-006`, `docs/RETOMADA.md`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/next.config.ts`, `infra/docker-compose.yml` e esta tarefa; relatório em `docs/reviews/004-frontend-e-raiz.md`.
- Dúvidas ou riscos: após autorização para interromper e reiniciar a prévia, `npm ci`, lint, typecheck e build passaram. A auditoria npm completa reporta 16 vulnerabilidades moderadas em dependências de desenvolvimento; `npm audit --omit=dev` reporta zero e `npm audit fix --dry-run` não encontra correção compatível. Fagner autorizou o CI a falhar a partir de severidade alta; nenhuma dependência foi atualizada. A sintaxe YAML do Compose foi validada, mas `docker compose config` não pôde rodar porque Docker CLI não está instalado. O ambiente bloqueia `git commit`; nenhum `git add` ou `git commit` foi executado.
