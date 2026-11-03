# Retomada do trabalho

Atualizado em 03/11/2026. Checkpoint curto: leia antes de retomar, junto com `CLAUDE.md` e a tarefa da vez. Atualize ao concluir ou pausar uma tarefa. Histórico até 02/11/2026: `docs/reviews/historico-retomada-ate-2026-11-02.md`.

## Estado atual
- **Ferramenta:** só Claude Code (Sonnet padrão, Haiku no `Explore`). OpenCode descontinuado; arquivos preservados até a decisão D-31 (o ciclo pago vence em até 2 semanas a partir de 03/11/2026).
- **Plano:** `docs/PLANO-MESTRE.md` v3.1 (correções da `docs/reviews/revisao-opus-001.md`).
- **Etapa 0, Fundação:** 003, 003B, 004, 004A, 004B e 005 concluídas (005 em `d10b2ad`: PostgreSQL, SQLAlchemy 2, Alembic, `audit_log` somente inserção, **sem RLS**).
- **005B** (multi-tenant e RLS): rascunho em `docs/tasks/005B-fundacao-multi-tenant-rls.md`, **não aprovada**. Falta incluir a resolução pré-contexto (plano §8 regra 8, S-40, D-32) e a ADR-007.
- **ADRs:** 001 a 006 em proposta; 007 a 009 não escritas.
- **Tarefas OpenCode 003C, 003D, 003F, 003H e 006 (superpowers):** encerrar como descontinuadas junto com D-31; não reconciliar.
- **CI remoto** do commit `d10b2ad`: não verificado (`gh` ausente).
- **Capacidade:** cerca de 25 h/semana. Teto de IA: US$ 50/mês (D-30). Beta: 1 ou 2 fotógrafos confirmados, que aceitam o B1 sem álbuns.

## Pendências do Fagner (fora do repositório)
1. `~/.claude/settings.json` está com JSON inválido (faltam `{` e `}`). Ao consertar, remover `CLAUDE_CODE_EFFORT_LEVEL: max` (sobrepõe `/effort`) e avaliar remover `CLAUDE_CODE_AUTO_COMPACT_WINDOW`.
2. Decisões D-27 a D-32 (plano §17) e as anteriores ainda abertas, sobretudo D-01, D-03, D-05, D-26.

## Pendências no repositório (não aplicadas nesta rodada)
- `.claude/settings.json`: acrescentar o deny de leitura de `.env` por Bash e PowerShell e `ask` para `git push` (texto na revisão Opus 001, §3).
- Skill `economia-de-tokens`: 4 ajustes de texto (revisão Opus 001, §3).

## Próximo passo
1. (Sonnet) Tarefa pequena: settings do projeto + skill, conforme a revisão Opus 001 §3.
2. (Sonnet + `postgres-dba`) Escrever a ADR-007 e revisar a 005B com S-40 e D-32. Apresentar ao Fagner para aprovação.
3. Após aprovação: implementar a 005B, fechar a Etapa 0 e começar a 006.
