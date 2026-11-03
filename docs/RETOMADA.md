# Retomada do trabalho

Atualizado em 03/11/2026. Checkpoint curto: leia antes de retomar, junto com `CLAUDE.md` e a tarefa da vez. Atualize ao concluir ou pausar uma tarefa. Histórico até 02/11/2026: `docs/reviews/historico-retomada-ate-2026-11-02.md`.

## Estado atual
- **Ferramenta:** só Claude Code (Sonnet padrão, Haiku no `Explore`). OpenCode descontinuado; arquivos preservados até a decisão D-31 (o ciclo pago vence em até 2 semanas a partir de 03/11/2026).
- **Plano:** `docs/PLANO-MESTRE.md` v3.1 (correções da `docs/reviews/revisao-opus-001.md`).
- **Etapa 0, Fundação: CONCLUÍDA em 03/11/2026.** 003–005 e a 005B (RLS forçada, papéis `pics_migration`/`app_runtime`/`pics_resolver`, funções definer de resolução, `tenancy.py`, 26 testes). Relatório: `docs/reviews/005B-fundacao-multi-tenant-rls.md`.
- **ADRs:** 001 a 006 em proposta; **007 aprovada**; 008 e 009 não escritas (008 antes da 029, 009 antes da 017).
- **Tarefas OpenCode 003C, 003D, 003F, 003H e 006 (superpowers):** encerrar como descontinuadas junto com D-31; não reconciliar.
- **CI remoto** do commit `d10b2ad`: não verificado (`gh` ausente).
- **Capacidade:** cerca de 25 h/semana. Teto de IA: US$ 50/mês (D-30). Beta: 1 ou 2 fotógrafos confirmados, que aceitam o B1 sem álbuns.

## Pendências do Fagner
1. Decisões D-27 a D-31 e as anteriores ainda abertas, sobretudo D-01, D-03, D-05, D-26. (D-32 aprovada.)
2. `git push` (nada foi enviado). Em ambiente com volume Docker antigo, rodar `infra/postgres/roles.sql` e definir senhas dos papéis fora do repositório.

## Próximo passo
Etapa 1, tarefa **006** (identidade e acesso). Ler as observações 3 a 5 do relatório 005B: `user_id` só da sessão, grants por coluna em `users`/`sessions`, startup falha se o papel da API for superusuário. Ver também a 006 de homologação OpenCode (descontinuada, D-31).
