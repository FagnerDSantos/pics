# ADR-005: Worker de processamento de imagens

- **Status:** Proposta — pendente de aprovação.
- **Contexto:** Geração de miniaturas e prévias pode exigir tempo e memória
  incompatíveis com uma requisição HTTP síncrona.
- **Proposta:** Processar imagens fora da requisição web, com limites explícitos
  de tamanho e pixels; validar conteúdo, corrigir orientação e remover EXIF dos
  derivados.
- **Consequências:** O fluxo precisa representar estados de processamento e falha;
  fila, retentativas e operação do worker serão definidos na implementação.
- **Revisão:** Validar limites e estratégia de execução antes de considerar esta
  decisão aprovada.
