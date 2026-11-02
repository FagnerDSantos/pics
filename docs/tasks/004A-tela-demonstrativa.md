# Tarefa 004A - Primeira tela demonstrativa do Pics

## Objetivo
Substituir a página boilerplate por uma tela inicial demonstrável do produto, para apresentar visualmente a direção do painel Pics. A tela usa somente dados fictícios e deixa claro que ainda é uma prévia estática, sem funcionalidades conectadas.

## Contexto
- M0 (fundação técnica) é o marco em andamento; a identidade visual definitiva será decidida na tarefa 020 (D-09).
- O pedido de Fagner é ter uma tela ou resultado visível já na próxima entrega.
- O frontend atual usa Next.js, React e Tailwind já declarados em `frontend/package.json`; não adicionar dependências, imagens externas nem tomar decisões definitivas de identidade visual.
- Esta tela é uma prévia provisória do painel, não implementa login, upload ou persistência.

## Critérios de aceite
- [x] A rota inicial apresenta um painel Pics responsivo e visualmente completo, em português do Brasil, com navegação, resumo e galerias ilustrativas.
- [x] Conteúdo e indicadores são explicitamente fictícios/demonstrativos; nenhuma ação sugere que upload, login ou persistência já estejam funcionais.
- [x] Usar ilustrações CSS/gradientes locais, sem fotografias reais, chamadas externas ou novas dependências.
- [x] A página é semântica e acessível por teclado; contraste e foco visível adequados; segue `prefers-reduced-motion`.
- [x] Definir idioma do documento como `pt-BR` e metadados descritivos em `frontend/src/app/layout.tsx`.
- [x] `npm run lint` e `npm run build` passam.
- [x] Atualizar `docs/RETOMADA.md` e criar `docs/reviews/004A-tela-demonstrativa.md`.

## Arquivos que podem ser alterados
- `frontend/src/app/page.tsx`
- `frontend/src/app/globals.css`
- `frontend/src/app/layout.tsx`
- `docs/tasks/004A-tela-demonstrativa.md`
- `docs/reviews/004A-tela-demonstrativa.md`
- `docs/RETOMADA.md`

## Fora de escopo
- Login, autorização, API, banco de dados, upload, pagamento ou dados reais.
- Definir a identidade visual final ou implementar as tarefas 020–022.
- Instalar/atualizar dependências ou alterar lockfiles.
- Alterar arquivos OpenCode, `.env`, infraestrutura ou CI.

## Regras de segurança aplicáveis
- Usar somente dados demonstrativos inventados; não incluir fotos reais, dados pessoais ou segredos.
- Não adicionar formulários ou ações que aparentem executar operações ainda inexistentes.
- Não acessar nem alterar `.env` ou os arquivos locais OpenCode preservados.

## Como testar
1. Executar `npm run lint` em `frontend/`.
2. Executar `npm run build` em `frontend/`.
3. Iniciar com `npm run dev` e conferir `http://localhost:3000` em viewport desktop e móvel.
4. Navegar com teclado e conferir foco, idioma e indicação de conteúdo demonstrativo.
5. Executar `git diff --check` e revisar se só os arquivos permitidos foram alterados.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito: idioma `pt-BR` e metadados descritivos; revisão de acessibilidade com atalho para o conteúdo principal, nomes/estrutura semântica, contraste dos textos secundários e remoção de link de demonstração sem destino funcional. Preservadas as ilustrações locais e a preferência por movimento reduzido.
- Arquivos alterados: `frontend/src/app/page.tsx`, `frontend/src/app/globals.css`, `frontend/src/app/layout.tsx`, `docs/tasks/004A-tela-demonstrativa.md`, `docs/reviews/004A-tela-demonstrativa.md` e `docs/RETOMADA.md`.
- Dúvidas ou riscos: não foram identificados bloqueios dentro do escopo demonstrativo. O ambiente bloqueia `git commit`; nenhum commit foi criado.
