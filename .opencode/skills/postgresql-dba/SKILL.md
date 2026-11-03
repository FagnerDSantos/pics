---
name: postgresql-dba
description: Padrões consultivos de PostgreSQL 16, SQLAlchemy 2 e Alembic para integridade multi-tenant, segurança e operações de banco.
---

# PostgreSQL DBA — padrões locais

Ative esta skill somente quando a tarefa a listar e após a permissão de skill existente. É referência consultiva: não autoriza execução de SQL, conexão a banco, instalação, migração ou mudança de privilégios.

## Escopo e limites

- Trabalhe apenas com schema, diff e fixtures textuais fictícias fornecidos na tarefa.
- Não leia `.env`, solicite credenciais/URLs de banco ou processe PII, fotos ou dados reais.
- Nunca conecte a banco real nem execute comandos. Não declare validações executadas sem evidência do executor.
- Mudanças em schema, migrações e privilégios exigem aprovação humana explícita antes de serem aplicadas.

## Tenancy e integridade

- Toda tabela de negócio contém `studio_id NOT NULL` e índice adequado ao padrão de consulta.
- Use chaves estrangeiras compostas com `studio_id` para impedir associações entre estúdios, além de unicidade e `CHECK` no banco quando aplicável.
- A aplicação valida autorização e estúdio em cada operação; RLS é uma segunda barreira, não substitui validações da aplicação.
- Ative RLS nas tabelas de negócio e avalie `FORCE ROW LEVEL SECURITY` para evitar bypass acidental pelo proprietário. Políticas devem negar acesso quando o contexto do estúdio estiver ausente e limitar linhas ao estúdio atual.
- O papel usado pela aplicação não pode ser superuser, proprietário das tabelas nem possuir `BYPASSRLS`; separe-o do papel de migração com privilégios estritamente necessários.
- Defina o contexto de tenancy com `SET LOCAL app.studio_id` dentro da transação/ conexão da requisição para evitar vazamento entre conexões reutilizadas. Considere o valor não confiável e mantenha SQL parametrizado.
- Sugira testes de isolamento que provem que A não lê, altera nem apaga dados de B, incluindo contexto ausente e referências cruzadas.

## SQLAlchemy 2 e Alembic

- Use consultas parametrizadas e APIs declarativas tipadas do SQLAlchemy 2; não monte SQL com interpolação de entrada.
- Revise o SQL gerado por autogenerate do Alembic: ele não substitui revisão de constraints, índices, RLS, políticas e privilégios.
- Faça migrações pequenas, determinísticas e compatíveis com a versão de aplicação em implantação; descreva precondições, efeitos, locks, duração esperada e recuperação.
- Prefira expand/contract para mudanças incompatíveis: adicionar estrutura compatível, migrar/validar, atualizar consumidores e só então remover estrutura antiga.
- Antes de operação destrutiva, exija aprovação, backup restaurável, contagens/validações de consistência, janela/estratégia de lock e plano de rollback. Não assuma que downgrade recupera dados apagados.
- Mantenha alterações transacionais quando possível. Identifique exceções PostgreSQL que não podem executar dentro de transação e exija plano específico revisado.
- Proteja tabelas append-only, como `audit_log`, com privilégios e controles no banco, não apenas convenções de aplicação.

## Consultas, índices e concorrência

- Proponha índices a partir de predicados e ordenações reais, geralmente começando por `studio_id` em acessos multi-tenant; evite índices redundantes e considere custo de escrita e armazenamento.
- Considere índices únicos compostos, `NULL`, collation e concorrência. Prefira constraints para invariantes que devam ser garantidos mesmo sob requisições concorrentes.
- Para avaliar planos, use apenas SQL e dados fictícios. `EXPLAIN ANALYZE` executa a consulta: não recomende executá-lo em operações mutáveis ou em dados reais sem autorização e salvaguardas.
- Use transações curtas, ordem consistente de locks, idempotência quando aplicável e tratamento explícito de deadlocks/serialização.

## Backup, restauração e exposição de dados

- Backup só é comprovado quando a restauração é testada e documentada; recomende teste em ambiente isolado com dados fictícios ou devidamente protegidos.
- Defina RPO/RTO, retenção, criptografia, acesso mínimo e verificações de integridade no plano operacional, sem incluir segredos na documentação.
- Logs e diagnósticos não devem expor credenciais, parâmetros pessoais, conteúdo de fotos nem linhas de negócio desnecessárias.
- Em resposta consultiva, cite `arquivo:linha` somente quando a localização estiver presente nos insumos; registre limitações quando ela não estiver.
