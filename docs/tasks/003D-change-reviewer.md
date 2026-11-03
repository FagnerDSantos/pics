# Tarefa 003D - Agente revisor geral de alterações

## Objetivo
Adicionar um agente revisor geral, somente leitura, para analisar cada diff contra a tarefa e seus critérios de aceite. O revisor complementa o `security-reviewer`; não substitui testes, lint nem a revisão do coordenador.

## Contexto
- O `security-reviewer` existente cobre apenas itens S-xx e recebe o diff no prompt porque não pode executar comandos.
- O fluxo em `CLAUDE.md` exige revisão do coordenador, mas não inclui um agente independente para revisar escopo, critérios, regressões e qualidade geral.
- O agente `build` é o executor. O revisor deve usar uma família de modelo diferente da família configurada para `build`.

## Critérios de aceite
- [x] Criar `.opencode/agent/change-reviewer.md` em modo `subagent`, somente leitura (`edit: deny`, `bash: deny`) e sem permissão para delegar tarefas.
- [x] Usar modelo gratuito de família diferente do agente `build`; registrar a escolha no relatório da tarefa. Não introduzir provedor pago nem nova dependência.
- [x] O prompt deve exigir do coordenador o diff completo, a tarefa/aceite e resultados de testes/lint; se faltar algum insumo, pedir antes de concluir.
- [x] Revisar cada critério de aceite, aderência ao escopo, regressões, segurança, tratamento de erros, tipos/lint/testes e documentação aplicáveis.
- [x] Achados devem citar `arquivo:linha`, severidade (`bloqueante`, `alta`, `média`, `baixa`) e correção sugerida em texto; não alterar arquivos nem executar comandos.
- [ ] Se não encontrar problemas, declarar explicitamente “nenhum achado” e listar os critérios revisados; não presumir que testes passaram sem receber seus resultados.
- [x] Atualizar o fluxo de `CLAUDE.md` para invocar o `change-reviewer` após o `build` e antes da aprovação/commit, fornecendo diff e resultados de validação.
- [x] `opencode agent list` mostra `change-reviewer (subagent)` e a configuração carrega sem erro.
- [ ] Validar a resposta com diff fictício contendo um problema intencional e conferir que o agente aponta o achado sem tentar corrigir.
- [x] Atualizar `docs/RETOMADA.md` e criar `docs/reviews/003D-change-reviewer.md`.

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

## Reconciliação documental — 2026-11-02

- `CLAUDE.md`, `docs/PLANO-MESTRE.md`, `docs/RETOMADA.md`, `docs/reviews/003D-change-reviewer.md` e `docs/reviews/003H-modelos-e-orquestrador-opencode.md` foram lidos antes desta atualização.
- A tarefa 003D teve o critério funcional bloqueado historicamente nesta sessão: invocação direta de `change-reviewer` caiu em fallback para o agente padrão, e chamadas pelo fluxo de delegação do `build` excederam 300 segundos sem retornar (registro original em `docs/reviews/003D-change-reviewer.md:15` e neste relatório).
- Posteriormente, na tarefa **003H**, o `change-reviewer` foi usado com sucesso via orquestrador para revisar a configuração do orquestrador e produzir achados (evidência em `docs/reviews/003H-modelos-e-orquestrador-opencode.md:26-27` e `docs/reviews/003H-modelos-e-orquestrador-opencode.md:31-34`). Esse fato é registrado como evidência disponível, mas **não comprova** os critérios específicos de 003D sobre:
  - [ ] revisão de diff sintético contendo bug intencional;
  - [ ] cenário sem achados com declaração explícita.
- **O teste funcional exigido não foi repetido agora.** A evidência 003H está disponível para avaliação humana, mas não substitui automaticamente os critérios funcionais acima.
- O critério de modelo gratuito (`opencode/glm-5.3-flash-free`) foi satisfeito historicamente na execução original, mas o alinhamento posterior de modelos alterou a escolha; esta reconciliação não afirma que o modelo atual é gratuito e não altera a configuração.
- Aprovação formal, DoD, commit e publicação permanecem pendentes.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito (execução original): criado o agente somente leitura e atualizado o fluxo do coordenador, incluindo uma regra para o agente `build` executar diretamente sem iniciar outra instância de `build`. A configuração do agente foi listada pelo CLI. Esta reconciliação documental não reexecutou essas ações.
- Arquivos alterados nesta reconciliação: este arquivo, `docs/reviews/003D-change-reviewer.md` e `docs/RETOMADA.md`. Arquivos originais da tarefa: `.opencode/agent/change-reviewer.md` e `CLAUDE.md`.
- Dúvidas ou riscos: critérios funcionais de validação com diff sintético e cenário sem achados permanecem pendentes. A evidência 003H demonstra uso sintético do `change-reviewer`, mas não repete os cenários específicos exigidos por 003D. Aprovação formal, DoD, commit e publicação continuam pendentes.
