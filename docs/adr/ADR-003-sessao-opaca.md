# ADR-003: Sessão opaca no servidor

- **Status:** Proposta — pendente de aprovação.
- **Contexto:** Sessões precisam ser revogáveis e não devem expor credenciais de
  longa duração ao navegador.
- **Proposta:** Manter o estado de sessão no servidor e entregar ao navegador
  apenas um identificador opaco em cookie `HttpOnly`, `Secure` e `SameSite=Lax`.
- **Consequências:** Revogação e expiração são controladas no servidor; armazenamento,
  rotação, CSRF e recuperação precisam ser definidos na implementação de acesso.
- **Revisão:** Validar modelo de ameaças e detalhes de sessão antes de considerar
  esta decisão aprovada.
