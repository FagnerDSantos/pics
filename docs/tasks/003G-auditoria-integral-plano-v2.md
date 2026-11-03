# Tarefa 003G - Auditoria integral pós Plano Mestre v2

## Objetivo
Verificar o estado real do monorepo e do fluxo de agentes contra `docs/PLANO-MESTRE.md` v2, executar as validações locais aplicáveis e registrar lacunas priorizadas sem afirmar conformidade além do que foi testado.

## Contexto
- O Plano Mestre v2 de 02/11/2026 redefine o produto como SaaS multi-tenant; cada tabela de negócio requer `studio_id`, RLS e testes de isolamento entre estúdios.
- O status v2 da seção 20 marca 003–005 como pendentes, enquanto tarefas/revisões anteriores indicam trabalho implementado; reconciliar fatos e documentação, sem presumir que o código satisfaz os requisitos novos.
- Fagner autorizou trabalho autônomo e verificações paralelas de agentes durante a janela desta sessão.

## Critérios de aceite
- [ ] Fazer inventário de backend, frontend, infra, CI, documentação e configuração OpenCode, sem ler `.env` ou credenciais.
- [ ] Comparar o código e as migrações atuais com o Plano Mestre v2, identificando especialmente `studio_id`, RLS, `BYPASSRLS`, chaves estrangeiras compostas, isolamento de consultas/storage e divergências do status/documentação.
- [ ] Delegar verificações independentes a `explore`, `general` e `security-reviewer`; registrar o pedido, a resposta e limitações de cada agente.
- [ ] Testar os agentes primários `plan` e `build` com prompts sintéticos sem alteração de arquivos.
- [ ] Testar `change-reviewer` e `postgres-dba` por uma via suportada de subagent, com achado sintético, somente após suas configurações existirem; diferenciar teste real de fallback ou timeout.
- [ ] Verificar `opencode agent list`, permissões efetivas e `opencode mcp list`; nenhum MCP deve ser conectado sem necessidade nesta tarefa.
- [ ] Executar validações locais disponíveis: backend (`ruff`, `mypy`, `pytest`), frontend (`npm run lint`, typecheck, build e auditoria npm conforme scripts disponíveis), CI/Compose config e `git diff --check`; registrar comandos não executados e motivos.
- [ ] Relatar falhas existentes como achados com `arquivo:linha`, evidência, severidade e recomendação; não alterar código de produto fora de uma tarefa aprovada.
- [ ] Criar matriz `Agente | Papel | Teste | Resultado | Bloqueio` e matriz de conformidade por área em `docs/reviews/003G-auditoria-integral-plano-v2.md`.
- [ ] Atualizar a seção 20 do Plano Mestre e `docs/RETOMADA.md` com os estados comprovados, sem marcar pendências como concluídas por inferência.

## Arquivos que podem ser alterados
- `docs/tasks/003G-auditoria-integral-plano-v2.md`
- `docs/reviews/003G-auditoria-integral-plano-v2.md`
- `docs/PLANO-MESTRE.md` (somente seção 20/status, com evidências)
- `docs/RETOMADA.md`
- Configuração OpenCode estritamente se necessário para corrigir um bloqueio de agente, e somente com registro no relatório.

## Fora de escopo
- Implementar autenticação, multi-tenancy, RLS, isolamento, rotas, billing ou qualquer feature de produto.
- Executar comandos contra produção, acessar dados reais, ler `.env` ou usar segredos.
- Instalar dependências, skills externas, plugins ou MCPs.
- Modificar schema/migrações ou apagar dados/bancos.
- Declarar pronto para beta/produção; esta tarefa é diagnóstico local.

## Regras de segurança aplicáveis
- Somente fixtures sintéticas; não expor DSN, tokens, dados pessoais ou fotos.
- `security-reviewer` recebe apenas diffs e conteúdo explicitamente seguro, sem segredos.
- Testes PostgreSQL locais usam apenas o ambiente sintético já configurado e não alteram dados persistentes; não executar limpeza destrutiva sem verificar o alvo.
- Não ligar MCPs para esta tarefa.

## Skills/MCPs
- Nenhuma skill ou MCP. O Plano Mestre v2 não autoriza `superpowers` por padrão; nenhuma skill é necessária para esta auditoria.

## Como testar
1. Executar o inventário e os comandos de validação listados acima, no diretório correto de cada pacote.
2. Invocar diretamente as ferramentas de subagent disponíveis nesta sessão e registrar seus resultados.
3. Para agentes OpenCode customizados, validar via ferramenta suportada de delegação; não contar `opencode run --agent` com um `subagent` como teste funcional.
4. Revisar cada achado e a matriz de agentes; executar `git diff --check`.

## Aprovação
Execução autorizada por Fagner em 02/11/2026 para uma janela autônoma de até 45 minutos, sem novas solicitações de aprovação durante a janela. As decisões de produto e segurança continuam limitadas ao escopo autorizado; alterações de produto ficam fora desta tarefa.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito:
- Arquivos alterados:
- Dúvidas ou riscos:
