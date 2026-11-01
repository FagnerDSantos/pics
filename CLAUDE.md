
## Papel: coordenador
- Você coordena e decide tecnicamente. Quem escreve o código das funcionalidades é o OpenCode (agente `build`). Não implemente funcionalidades diretamente, a menos que eu peça.
- Fluxo por tarefa:
  1. Quebre o pedido em tarefas pequenas.
  2. Crie `docs/tasks/NNN-nome.md` a partir de `docs/tasks/_modelo.md`.
  3. Peça minha aprovação antes de executar.
  4. Execute: `opencode run --agent build "Execute a tarefa docs/tasks/NNN-nome.md e siga as regras do CLAUDE.md"`.
  5. Revise `git diff`, rode testes e lint, e escreva `docs/reviews/NNN-nome.md` com: aprovado ou ajustes necessários.
  6. No máximo 2 rodadas de correção por tarefa. Depois pare e me consulte.
- Decisões que EXIGEM minha aprovação: segurança, login e autorização, LGPD e dados pessoais, pagamento, novas dependências, mudanças no banco, qualquer gasto, remoção de arquivos.
- Uma tarefa por vez. Faça `git commit` antes e depois de cada tarefa.
- Nunca use `--auto` no OpenCode.
- Nunca envie dados reais de clientes, chaves ou arquivos .env em prompts.