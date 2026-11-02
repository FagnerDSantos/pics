# Tarefa 003D - Agente revisor geral de alterações

## Objetivo
Adicionar um agente revisor geral, somente leitura, para analisar cada diff contra a tarefa e seus critérios de aceite. O revisor complementa o `security-reviewer`; não substitui testes, lint nem a revisão do coordenador.

## Contexto
- O `security-reviewer` existente cobre apenas itens S-xx e recebe o diff no prompt porque não pode executar comandos.
- O fluxo em `CLAUDE.md` exige revisão do coordenador, mas não inclui um agente independente para revisar escopo, critérios, regressões e qualidade geral.
- O agente `build` é o executor. O revisor deve usar uma família de modelo diferente da família configurada para `build`.

## Critérios de aceite
- [ ] Criar `.opencode/agent/change-reviewer.md` em modo `subagent`, somente leitura (`edit: deny`, `bash: deny`) e sem permissão para delegar tarefas.
- [ ] Usar modelo de família diferente do agente `build`; registrar a escolha no relatório da tarefa. Não introduzir provedor pago nem nova dependência sem aprovação.
- [ ] O prompt deve exigir do coordenador o diff completo, a tarefa/aceite e resultados de testes/lint; se faltar algum insumo, pedir antes de concluir.
- [ ] Revisar cada critério de aceite, aderência ao escopo, regressões, segurança, tratamento de erros, tipos/lint/testes e documentação aplicáveis.
- [ ] Achados devem citar `arquivo:linha`, severidade (`bloqueante`, `alta`, `média`, `baixa`) e correção sugerida em texto; não alterar arquivos nem executar comandos.
- [ ] Se não encontrar problemas, declarar explicitamente “nenhum achado” e listar os critérios revisados; não presumir que testes passaram sem receber seus resultados.
- [ ] Atualizar o fluxo de `CLAUDE.md` para invocar o `change-reviewer` após o `build` e antes da aprovação/commit, fornecendo diff e resultados de validação.
- [ ] `opencode agent list` mostra `change-reviewer (subagent)` e a configuração carrega sem erro.
- [ ] Validar a resposta com diff fictício contendo um problema intencional e conferir que o agente aponta o achado sem tentar corrigir.
- [ ] Atualizar `docs/RETOMADA.md` e criar `docs/reviews/003D-change-reviewer.md`.

## Arquivos que podem ser alterados
- `.opencode/agent/change-reviewer.md`
- `CLAUDE.md`
- `docs/tasks/003D-change-reviewer.md`
- `docs/reviews/003D-change-reviewer.md`
- `docs/RETOMADA.md`

## Fora de escopo
- Alterar código de `backend/` ou `frontend/`.
- Substituir, remover ou ampliar o papel do `security-reviewer`.
- Adicionar dependências, plugins ou MCPs.
- Fazer o revisor executar lint/testes ou editar/corrigir achados.
- Alterar o escopo do produto ou o roadmap mestre.

## Regras de segurança aplicáveis
- Dados de teste e diffs de validação devem ser fictícios.
- Não enviar `.env`, segredos, fotos reais ou dados pessoais ao modelo revisor.
- O agente não pode editar, executar Bash nem delegar tarefas.
- Selecionar modelo de família diferente do `build`; confirmar custo e política de dados antes de escolher modelo não gratuito.
- O coordenador continua responsável por executar validações e decidir se aceita a revisão.

## Como testar
1. Inspecionar o frontmatter e as permissões de `.opencode/agent/change-reviewer.md`.
2. Executar `opencode agent list` e confirmar `change-reviewer (subagent)`.
3. Enviar diff sintético com um bug simples e confirmar achado `arquivo:linha`, severidade e recomendação sem edição/comando.
4. Confirmar que `CLAUDE.md` torna a revisão uma etapa antes de concluir cada tarefa.
5. Executar `git diff --check` e revisar que não há alterações fora dos arquivos permitidos.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito:
- Arquivos alterados:
- Dúvidas ou riscos:
