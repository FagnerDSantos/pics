# Tarefa 003E - Marcos de entrega do produto

## Objetivo
Organizar o roadmap do Pics em marcos de entrega verificáveis, mantendo as tarefas 003–025 e seus escopos atuais. Registrar no plano mestre os entregáveis, critérios de conclusão, dependências e pontos de decisão de cada marco.

## Contexto
- `docs/PLANO-MESTRE.md`, seções 14, 15 e 18, contém o roadmap por tarefa e decisões de produto pendentes.
- `docs/RETOMADA.md` registra que Fagner concordou com a organização por marcos, mas que a decomposição e os critérios ainda precisam ser decididos.
- Este documento propõe a seguinte estrutura para aprovação antes de atualizar o plano mestre:

| Marco | Tarefas | Entrega proposta |
|---|---|---|
| M0 — Fundação técnica | 003–005 | Monorepo, CI e ambiente local reproduzíveis; frontend estruturado; PostgreSQL, SQLAlchemy e migrações funcionando. |
| M1 — Identidade e acesso | 006–009 | Acesso de admin e cliente, sessões, proteção contra abuso, autorização por papel e recurso, 2FA de admin e consentimento inicial. |
| M2 — Galerias e fotos | 010–014 | Upload privado, processamento seguro, prévias com marca d'água, publicação, acesso do cliente e expiração automatizada. |
| M3 — Álbuns | 015–017 | Seleção, montagem por lâminas, prova para aprovação e pacote de produção exportável. |
| M4 — Pagamento e entrega | 018–019 | Pedido e Pix integrado, webhook verificado e idempotente, liberação pós-pagamento e registro de downloads. |
| M5 — Site e experiência visual | 020–022 | Identidade visual aprovada, site institucional e experiência coerente nas áreas logadas; pode avançar em paralelo após 013. |
| M6 — LGPD e pré-lançamento | 023–025 | Direitos do titular, retenção, revisão de segurança, recuperação testada, operação e deploy preparados para lançamento. |

## Critérios de aceite
- [x] Fagner aprova a divisão, os nomes, o escopo e a ordem/dependências propostas antes da incorporação ao plano mestre.
- [x] O plano mestre associa cada tarefa do roadmap da seção 14 a um único marco, sem alterar o escopo funcional já aprovado.
- [x] Cada marco recebe entregáveis e critérios de conclusão verificáveis; concluir tarefas isoladas não basta para declarar o marco concluído.
- [x] Definir critério comum para concluir cada marco: todas as tarefas associadas atendem aos próprios critérios de aceite e ao DoD da seção 13; documentação e revisão correspondentes estão atualizadas.
- [x] Critérios específicos registrados:
  - [x] M0: instalação e execução local documentadas; migrações e testes de integração do banco passam; CI executa as verificações definidas para backend e frontend.
  - [x] M1: fluxos de acesso funcionam conforme os papéis; testes cobrem não autenticado, papel incorreto e acesso a recurso alheio nas rotas protegidas.
  - [x] M2: ciclo upload → processamento → publicação → visualização autorizada → expiração é validado; originais permanecem privados e inacessíveis antes do pagamento.
  - [x] M3: limites e transições do álbum são validados no servidor; prova, aprovação e exportação correspondem à seleção e à ordem final.
  - [x] M4: integração usa ambiente de testes do provedor escolhido; webhook tem assinatura e idempotência verificadas; download só é liberado após pagamento confirmado.
  - [x] M5: páginas e áreas previstas estão responsivas e acessíveis; conteúdo legal aguarda revisão jurídica quando aplicável; validações de tipo, lint e build passam.
  - [x] M6: solicitações LGPD e retenção estão exercitáveis; restauração de backup foi testada; revisão de segurança e checklist de lançamento não têm bloqueios abertos.
- [x] O plano registra dependências e trilhas paralelas: M0 → M1 → M2; M3 após o fluxo de seleção; M4 após o fluxo de álbum; M5 pode iniciar após 013; M6 é gate de lançamento.
- [x] Decisões pendentes da seção 15 são associadas aos marcos/tarefas que dependem delas, sem presumir decisões ainda não aprovadas.
- [x] Atualizar `docs/RETOMADA.md` e criar `docs/reviews/003E-marcos-entrega.md` com a decisão final e o próximo passo.

## Arquivos que podem ser alterados
- `docs/PLANO-MESTRE.md`
- `docs/RETOMADA.md`
- `docs/tasks/003E-marcos-entrega.md`
- `docs/reviews/003E-marcos-entrega.md`

## Fora de escopo
- Alterar código do backend, frontend ou configuração OpenCode.
- Reordenar ou reescrever requisitos funcionais, segurança, LGPD ou arquitetura.
- Resolver decisões pendentes D-01 a D-11 ou iniciar as tarefas de implementação.
- Adicionar dependências, custos ou compromissos de prazo.

## Regras de segurança aplicáveis
- Não registrar segredos, dados pessoais, fotos reais ou conteúdo de `.env`.
- Não marcar decisões de produto ou jurídicas como aprovadas sem aprovação explícita de Fagner.
- Preservar todas as alterações locais existentes fora dos arquivos explicitamente listados.

## Como testar
1. Conferir se todas as tarefas do roadmap da seção 14 aparecem uma única vez na divisão aprovada.
2. Conferir consistência dos marcos com o roadmap, decisões pendentes e status da seção 18.
3. Executar `git diff --check` e revisar o diff para confirmar que apenas os arquivos permitidos foram alterados.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito: registrou os marcos M0–M6 aprovados, critérios, dependências, decisões e status inicial.
- Arquivos alterados: `docs/tasks/003E-marcos-entrega.md`, `docs/PLANO-MESTRE.md`, `docs/RETOMADA.md`, `docs/reviews/003E-marcos-entrega.md`.
- Dúvidas ou riscos: a execução da tarefa 003D e o plugin local de fallback continuam como decisões independentes.
