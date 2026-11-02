# ADR-004: Storage privado e URLs assinadas

- **Status:** Proposta — pendente de aprovação.
- **Contexto:** Originais e prévias são arquivos privados, com permissões e ciclos
  de vida diferentes.
- **Proposta:** Usar storage S3-compatível privado e URLs assinadas de curta
  duração, emitidas pela API somente após autorização; MinIO fica reservado ao
  desenvolvimento local.
- **Consequências:** O bucket não é público e a aplicação controla emissão,
  expiração e escopo das URLs. O provedor de produção depende da decisão D-02.
- **Revisão:** Validar políticas de acesso, chaves, retenção e provedor antes de
  considerar esta decisão aprovada.
