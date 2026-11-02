# ADR-002: PostgreSQL, SQLAlchemy 2 e Alembic

- **Status:** Proposta — pendente de aprovação.
- **Contexto:** O produto precisa persistir usuários, galerias, fotos, pedidos e
  registros de auditoria com integridade transacional.
- **Proposta:** Usar PostgreSQL como banco relacional, SQLAlchemy 2 como ORM e
  Alembic para migrações versionadas.
- **Consequências:** Esquema e migrações ficam explícitos e revisáveis; operação,
  backups, transações e testes de integração precisam acompanhar a evolução.
- **Revisão:** Validar o modelo e as práticas operacionais antes de considerar
  esta decisão aprovada.
