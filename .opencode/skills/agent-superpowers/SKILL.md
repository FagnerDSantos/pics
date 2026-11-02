---
name: agent-superpowers
description: Capacidades avançadas de agentes: decomposição de tarefas complexas, checagens autonomas, iteração sistemática e validação rigorosa.
---
# Diretrizes de Agente (Superpowers)
- **Decomposição Modular:** Divida tarefas complexas em etapas autonomas, validadas uma a uma.
- **Raciocínio Orientado a Evidências:** Nunca assuma que uma alteração funcionou sem rodar linters, testes ou comandos de verificação de sintaxe.
- **Auto-Correção e Retentativas:** Diante de falhas ou erros de execução, inspecione a causa raiz, revise o código afetado e aplique a correção sem intervenção desnecessária do usuário.
- **Saídas Determinísticas:** Mantenha alterações focadas estritamente no escopo da tarefa informada, evitando reestruturações desnecessárias fora do plano.