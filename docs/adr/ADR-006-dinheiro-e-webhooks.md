# ADR-006: Dinheiro em centavos e webhooks idempotentes

- **Status:** Proposta — pendente de aprovação.
- **Contexto:** Valores monetários e eventos de provedores de pagamento precisam
  de representação precisa e processamento seguro contra reenvios.
- **Proposta:** Representar dinheiro como inteiro em centavos e processar webhooks
  com verificação de assinatura e idempotência persistida.
- **Consequências:** Cálculos não usam ponto flutuante; identificadores de evento
  e restrições únicas são necessários para impedir efeitos duplicados.
- **Revisão:** Validar provedores, arredondamento e política de eventos antes de
  considerar esta decisão aprovada.
