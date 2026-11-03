# Tarefa 003F - Agente DBA e simplificação da configuração de agentes

## Objetivo
Enxugar a configuração de agentes específica do projeto e adicionar um subagente especializado em PostgreSQL, migrações, integridade e segurança do banco. Criar uma skill local `postgresql-dba`, sem instalar skills externas.

## Contexto
- Pedido de Fagner: priorizar agentes para execução e revisão, reservando o coordenador para decisões; remover configurações de agentes sem uso e criar um agente DBA.
- `build`, `plan`, `explore` e `general` são agentes integrados do OpenCode; o repositório configura permissões/modelos para alguns deles, mas não os define como arquivos personalizados.
- `security-reviewer` e `change-reviewer` são revisores personalizados. O `general` é redundante para o fluxo do projeto; sua configuração específica pode ser removida e o uso como subagente bloqueado, embora o agente integrado ainda possa aparecer no CLI.
- O Plano Mestre v2 exige `studio_id` em toda tabela de negócio, RLS, papel da aplicação sem `BYPASSRLS`, chaves estrangeiras compostas e testes de isolamento entre estúdios (seções 6, 9 e 13).
- Mudanças de schema/banco continuam exigindo aprovação explícita. A skill deve ser local, alinhada à stack PostgreSQL 16, SQLAlchemy 2 e Alembic, e só deve ser carregada por tarefas que a listem.

## Critérios de aceite
- [x] Inventariar agentes integrados e personalizados em `opencode agent list`, `.opencode/agent/`, `opencode.json` e `CLAUDE.md`; documentar a distinção entre remover configuração do projeto e remover agente integrado do OpenCode.
- [x] Remover do projeto a configuração/referência redundante de `general` e impedir sua delegação como subagente, sem tentar apagar componentes internos do OpenCode.
- [x] Preservar `build`, `plan`, `explore`, `security-reviewer` e `change-reviewer`; documentar seus usos práticos no fluxo para reduzir a carga do coordenador.
- [x] Criar `.opencode/agent/postgres-dba.md` como `subagent` especializado em desenho/revisão de schema PostgreSQL, integridade, SQLAlchemy/Alembic, consultas/índices, permissões, segurança, backup e recuperação, com foco nos requisitos multi-tenant do Plano Mestre v2.
- [x] O agente DBA é consultivo e somente leitura (`read`, `edit`, `bash`, `task` e `skill` negados); analisa apenas insumos enviados pelo coordenador e sugere migrações/ajustes, sem aplicá-los.
- [x] Usar modelo disponível gratuito, de família diferente do executor `build`; não adicionar dependências nem provedor pago. **Nota de reconciliação:** este critério foi satisfeito historicamente na execução original com o modelo então registrado (`opencode/glm-5.3-flash-free`). Posteriormente, os modelos foram alinhados por decisão autorizada do usuário aos IDs declarados em \`opencode.json\` (ver \`docs/reviews/003H-modelos-e-orquestrador-opencode.md\`); a configuração atual do \`postgres-dba\` não é afirmada como gratuita e não é objeto desta reconciliação. Não reabrir a configuração de modelos sem nova aprovação explícita.
- [x] O DBA não lê `.env`, não recebe credenciais, dados reais ou PII, não se conecta a bancos reais e não executa comandos; alterações ou aplicação de migrações continuam sob aprovação humana explícita.
- [x] Criar `.opencode/skills/postgresql-dba/SKILL.md` com padrões locais para PostgreSQL 16, `studio_id`, RLS e papel sem `BYPASSRLS`, chaves compostas, testes de isolamento, migrações reversíveis/seguras, menor privilégio, transações, índices, backup/restauração e prevenção de exposição de dados; não usar conteúdo externo não aprovado.
- [x] A skill só pode ser ativada por tarefa que a liste e após o gate de permissão existente.
- [x] Atualizar `CLAUDE.md` para consultar o DBA em tarefas que alterem schema, migrações, permissões, consultas críticas ou controles do banco; o DBA recomenda e o coordenador aceita/rejeita antes de solicitar correções ao `build`.
- [ ] `opencode agent list` mostra `postgres-dba (subagent)` e confirma permissões somente leitura; o agente responde a um cenário sintético de migração arriscada sem executar nem editar. A listagem e permissões foram confirmadas na execução original. Há **evidência posterior disponível na tarefa 003H**: o orquestrador encaminhou ao `postgres-dba` uma proposta sintética de remover `studio_id`; o DBA recomendou bloquear a migração, sem editar arquivos, sem usar Bash e sem acessar dados reais (ver `docs/reviews/003H-modelos-e-orquestrador-opencode.md`). **O teste funcional não foi repetido agora.** A suficiência dessa evidência indireta para aceitar este critério **aguarda aprovação formal do usuário**.
- [x] Validar a estrutura da skill e atualizar `docs/RETOMADA.md` e `docs/reviews/003F-dba-e-simplificacao-agentes.md`.

## Arquivos que podem ser alterados
- `.opencode/agent/postgres-dba.md`
- `.opencode/skills/postgresql-dba/SKILL.md`
- `opencode.json`
- `CLAUDE.md`
- `docs/tasks/003F-dba-e-simplificacao-agentes.md`
- `docs/reviews/003F-dba-e-simplificacao-agentes.md`
- `docs/RETOMADA.md`

## Fora de escopo
- Executar migrations, consultas ou comandos contra qualquer banco de dados.
- Alterar schema, migrations, models, código de aplicação ou dados; o agente apenas recomenda.
- Remover os agentes integrados `build`, `plan` ou `explore`.
- Instalar skill, plugin, MCP, dependência ou modelo pago.
- Alterar as responsabilidades dos revisores de segurança e de mudanças.

## Regras de segurança aplicáveis
- Nenhum segredo, URL/credencial de banco, dado pessoal ou dado real em prompts, skill, teste, log ou documentação.
- O DBA não pode editar, executar Bash, delegar, conectar-se a banco ou carregar `.env`.
- DDL, migrações e mudanças de privilégios são propostas apenas; aprovação do Fagner continua obrigatória antes da execução.
- Skills/MCPs só podem ser usados se listados nesta tarefa e autorizados pelas permissões locais.

## Como testar
1. Inspecionar os agentes e as permissões efetivas com `opencode agent list`.
2. Confirmar que o agente integrado `general` não está mais configurado/delegável pelo projeto; registrar que ele ainda pode aparecer como built-in do CLI.
3. Inspecionar o frontmatter e o conteúdo da skill local, sem buscar conteúdo externo.
4. Enviar ao DBA um diff sintético contendo uma migração destrutiva e confirmar que aponta o risco e sugere mitigação, sem executar ou editar.
5. Executar `git diff --check` e revisar os arquivos dentro do escopo permitido.

## Aprovação
Fagner autorizou trabalho autônomo por até 45 minutos em 02/11/2026, incluindo limpeza de configuração de agentes e criação do DBA/skill conforme este escopo. Executar apenas dentro dos arquivos permitidos; não alterar nem conectar a banco de dados.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito: removida a configuração específica de `general`, com delegação negada em `opencode.json`; documentados os papéis dos agentes e a consulta consultiva ao DBA; criado o subagent PostgreSQL e a skill local `postgresql-dba`.
- Arquivos alterados nesta tarefa: `.opencode/agent/postgres-dba.md`, `.opencode/skills/postgresql-dba/SKILL.md`, `opencode.json`, `CLAUDE.md`, este arquivo, `docs/reviews/003F-dba-e-simplificacao-agentes.md` e `docs/RETOMADA.md`. Alterações pré-existentes em outros arquivos foram preservadas; nenhum `git add`, commit ou push foi feito.
- Validações reais: `opencode agent list` listou `postgres-dba (subagent)` e mostrou `read`, `edit`, `bash`, `task` e `skill` negados; também mostrou `general` ainda como agente integrado e a delegação para `general` negada. `opencode.json` passou por `ConvertFrom-Json` e checagem de ausência de `agent.general`/presença de `permission.task.general=deny`. A estrutura e o conteúdo da skill/agente foram inspecionados; `git diff --check` passou (com avisos do Git sobre LF/CRLF em arquivos modificados).
- Reconciliação documental: o critério funcional do `postgres-dba` estava bloqueado nesta sessão porque `functions.task` rejeitou o tipo configurado. Posteriormente, na tarefa **003H**, o orquestrador invocou o `postgres-dba` com sucesso: proposta sintética de remover `studio_id` foi encaminhada; o DBA recomendou bloquear a migração; não editou arquivos, não usou Bash e não acessou dados reais. A evidência está em `docs/reviews/003H-modelos-e-orquestrador-opencode.md`. **O teste funcional não foi repetido agora.**
- Pendências: revisão final, aprovação formal, `git add`/`commit`/`push` e declaração de DoD/publicação/tarefa concluída continuam pendentes. O modelo gratuito originalmente registrado foi substituído pelo alinhamento atual; esta reconciliação não reabre a decisão de modelo nem altera a configuração.

## Próximos passos

1. **Aprovação humana explícita** da reconciliação documental da 003F e da suficiência da evidência indireta proveniente da 003H para aceitar o critério funcional do `postgres-dba`.
2. **Decidir** se a 003F será considerada concluída sem novo teste funcional repetido agora, ou se será exigida uma nova invocação direta do `postgres-dba` após reinício do runtime.
3. **Reinício/verificação runtime manual do usuário** (não executar automaticamente): abrir uma nova sessão OpenCode para recarregar a configuração atual e confirmar que `postgres-dba` é listado corretamente.
4. **`git add`/`commit`/`push` da 003F somente após aprovação explícita** e com escopo isolado das preexistências do working tree. Não declarar a tarefa formalmente concluída antes disso.
