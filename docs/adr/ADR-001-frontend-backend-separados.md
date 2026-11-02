# ADR-001: Frontend e backend separados

- **Status:** Proposta — pendente de aprovação.
- **Contexto:** O Pics possui uma interface Next.js e uma API FastAPI, com
  necessidades e ciclos de entrega próprios.
- **Proposta:** Manter frontend e backend como aplicações separadas, comunicando-se
  pela API HTTP, mesmo estando no mesmo monorepo.
- **Consequências:** Cada camada pode evoluir e ser validada independentemente;
  contratos da API precisam ser tratados explicitamente. A proposta não define
  hospedagem nem repositórios separados.
- **Revisão:** Validar limites entre as camadas e estratégia de deploy antes de
  considerar esta decisão aprovada.
