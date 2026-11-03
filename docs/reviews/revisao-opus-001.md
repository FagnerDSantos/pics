# Revisão Opus 001: plano v3, agentes e ferramentas

Data: 03/11/2026 · Revisor: Claude Opus 5.5 (uso aprovado pelo Fagner) · Só análise, sem mudanças de código ou config.
Lidos: `CLAUDE.md`, `docs/PLANO-MESTRE.md` (v3), `docs/RETOMADA.md`, `docs/tasks/005B` (trechos), `.claude/` (agentes, skill, settings), `opencode.json`, `.opencode/agent/*`, `AGENTS.md`.
**Faltou `docs/origem/`**: não existe no repositório. Sem os documentos de origem, a comparação v3 × origem (item A) não foi feita; usei a tabela §0.3 do plano como referência.
Entrevista: teto de US$ 50/mês; falhas anteriores = lentidão e código de baixa qualidade; OpenCode Go vence em até 2 semanas e fica parado; 1 ou 2 fotógrafos para o beta, que aceitam o B1 sem álbuns.

## 1. Veredito
1. O B1 ainda não pode começar. A Etapa 0 está incompleta: RLS e multi-tenant (005B) estão em rascunho, não aprovados.
2. O plano v3 é sólido para um MVP. Faltam reembolso/estorno de Pix, o lookup pré-contexto sob RLS (cliente sem login e webhook) e a quebra de 012 e 016.
3. A config tem um risco de custo (`effort max` global) e uma brecha de segredo (o deny de `.env` não cobre Bash nem PowerShell).
4. Decisão sobre ferramentas: **só Claude Code**. O OpenCode fica parado até vencer e depois é arquivado.
5. Bloqueia o B1: aprovar 005B com o lookup resolvido, alinhar a documentação (RETOMADA e roadmap) e corrigir os settings.

## 2. Lacunas e contradições

### Crítico
- **C1. Roadmap × realidade (§16, §20, RETOMADA).** A §16 diz que a 005 entrega "RLS e papel sem `BYPASSRLS`", mas isso foi para a 005B (rascunho). A 005B não aparece no roadmap nem no mapa §0.2. A RETOMADA ainda manda "o agente `build`" implementar, fala em "marcos M0–M6, seções 14 e 18" (v2) e tem ~120 linhas de histórico do OpenCode.
  **Correção:** na §16 Etapa 0, a 005 fica "integração, sem RLS" e entra "**005B** Multi-tenant: `studios`, `studio_members`, roles, RLS fail-closed, testes A/B". Reescrever a RETOMADA em ≤40 linhas (estado atual + próximo passo) e mover o histórico para `docs/reviews/`.
- **C2. Lookup antes do contexto de estúdio (§8 regra 3, §10, 005B).** Com RLS fail-closed, a API precisa do `studio_id` *antes* de `SET LOCAL`, em três fluxos que o plano não resolve: (a) cliente final abre o link (`client_access.token_hash` é tabela de tenant); (b) webhook do Pix chega só com `provider_ref`; (c) login de usuário com vários estúdios. Além disso, `webhook_events` não tem `studio_id` nem classificação.
  **Correção:** adicionar ao 005B e ao §10 uma regra explícita. Resolução por **função `SECURITY DEFINER` mínima** (`resolve_client_token(hash) → (studio_id, gallery_id)`, `resolve_payment_ref(provider, ref) → studio_id`), com dono sem login, `search_path` fixo e teste. Ou uma tabela global de roteamento (`access_routes`: hash → studio_id) sem dados pessoais. Classificar `webhook_events` como global (sem PII; só `payload_hash`). O `postgres-dba` valida.
- **C3. Custo: `CLAUDE_CODE_EFFORT_LEVEL=max` em `~/.claude/settings.json`.** Essa variável tem prioridade sobre `/effort` (doc model-config/env-vars). Assim, **todas** as sessões rodam em `max`, o que contraria a skill ("evite xhigh e max") e o teto de US$ 50. O arquivo também está com JSON inválido (faltam `{` e `}`) e, por isso, hoje é ignorado. Ao consertar, o `max` passa a valer.
  **Correção (pede confirmação, é config global):** remover a linha ou trocar por `"medium"`. Avaliar também `CLAUDE_CODE_AUTO_COMPACT_WINDOW=786432`: uma janela grande deixa o contexto crescer e cada mensagem fica mais cara. Sugiro remover (usa o padrão).

### Alto
- **A1. Reembolso, estorno e MED do Pix (§4.7, §10).** `orders.status` tem `refunded`, mas não há fluxo, tabela nem regra para o que acontece com a liberação. **Correção:** tabela `refunds` (studio_id, payment_id, amount_cents, reason, provider_ref, status), webhook de devolução idempotente e **recálculo de `financial_status`**. Se o evento sair de QUITADO, `release.py` nega e os links ativos são revogados. Incluir na matriz §4.3 a linha "após estorno". Entra na 016 → **D-27**.
- **A2. Cancelamento de evento/pedido e saldo não pago (D-18).** Sem regra, o worker de expiração não sabe o que fazer. Definir antes da 016.
- **A3. Tarefas grandes demais para uma sessão.** 012 (clientes + pacotes + eventos + galerias + estados) → 012a modelos e CRUD, 012b máquina de estados e publicar. 016 (Pix inteiro) → 016a `orders/payments/webhook_events` + provedor *fake* + idempotência; 016b provedor real em sandbox (depende de D-01). 007 (RBAC + isolamento + audit + logging + suporte) → 007a RBAC e isolamento, 007b audit, logging e acesso de suporte.
- **A4. Ordem das dependências (§16).** A 010 impõe cotas, mas `plans` e assinatura só chegam na 020: na 010 use um **plano padrão semeado** e deixe a cobrança na 020. A 009 (link mágico) envia e-mail, mas o e-mail só aparece na 015 e D-03 está aberta: dev com Mailpit desde a 009, e D-03 decidida antes da 021. Webhook de assinatura (S-16) fica na 020 sem bloqueio.
- **A5. Retenção sem campos de estado (§4.6, §10).** Faltam `photos.original_deleted_at`, `photo_derivatives.expires_at/deleted_at` e `edited_files.deleted_at`. Sem eles, `studio_usage` não pode ser recalculado com segurança e a reabertura não sabe se ainda há original. Acrescentar também a recontagem periódica de `studio_usage` (fonte da verdade = soma no banco).
- **A6. ADRs 007–009 não existem** (`docs/adr/` tem 001–006). A ADR-007 (multi-tenancy + RLS) precisa estar aprovada **antes** da 005B.

### Médio
- **M1. Cliente sem e-mail:** o fotógrafo copia o link de acesso e envia por WhatsApp manualmente (sem integração) → **D-28**.
- **M2. Editor que estoura o prazo (pacote B "dentro do prazo"):** sem regra nem notificação → **D-29**.
- **M3. Notificações ao fotógrafo** (seleção confirmada, pagamento recebido, prazo vencendo) não estão em nenhuma tarefa. Incluir na 015 (só e-mail).
- **M4. Duplicatas:** `photos.sha256` existe sem regra. Avisar no upload e criar índice `(studio_id, gallery_id, sha256)` sem unicidade forçada.
- **M5. Formatos:** declarar no §11 "RAW, HEIC e vídeo fora do B1; editadas também só JPEG/PNG". Validar o tipo também em `edited_files`.
- **M6. Abuso:** "alertar acessos em massa" (§11) e o limite de downloads por link não têm tarefa. Pôr na 017 (contador por `client_access` + rate limit S-04).
- **M7. Filtros na galeria do cliente** (todas / favoritas / selecionadas) e no painel do fotógrafo: explicitar na 013/014.
- **M8. Matriz §4.3 "Confirmar seleção em PENDENTE: Não (sugerido)"** ainda é decisão em aberto. Incluir em D-22.
- **M9. Skills do §15** (`lgpd-data-mapping`, `lgpd-consent-schema`, `lgpd-dsar`, `lgpd-audit`, `security-audit`) não existem em `.claude/skills/`. Trocar por "a definir" ou instalar com aprovação. Lembrete: o OpenCode lê `.claude/skills`, mas o Claude Code não lê `.opencode/skills`.
- **M10. `CLAUDE.md` linha "Checks":** os comandos reais (RETOMADA) são `ruff check app tests`, `mypy app`, `pytest` e `npm run typecheck`. Corrigir.
- **M11. Suporte ao estúdio:** não há canal (e-mail de suporte basta no beta). Citar na 021.

## 3. Agentes, settings e skill (conferido em code.claude.com em 02/11/2026)
- **`.claude/settings.json` (projeto). Brecha:** `Read(...)` em deny bloqueia Read, Edit, Write, @-menções e, como melhor esforço, Grep e Glob. **Não bloqueia Bash nem PowerShell** (`cat .env`, `Get-Content .env`). Proposta de acréscimo ao `deny`:
  `"Bash(cat *.env*)", "Bash(type *.env*)", "Bash(*printenv*)", "PowerShell(Get-Content *.env*)", "PowerShell(gc *.env*)", "PowerShell(cat *.env*)"`, mais `"Read(**/*.pem)", "Read(**/*.key)"`, e `"ask": ["Bash(git push*)", "PowerShell(git push*)"]`.
  Aviso honesto: regras de Bash casam texto e **não são fronteira**. A defesa real é o `.env` de dev ter só valores sintéticos, e segredos reais ficarem fora do repositório.
  Não usar `Read(**/.env.*)`: o deny vence o allow e bloquearia o `.env.example`.
- **`CLAUDE_CODE_SUBAGENT_MODEL=sonnet`** é só o fallback (ordem: parâmetro da chamada > `model:` do agente > variável > modelo principal). **Não** força o `Explore` para Sonnet: ele segue em Haiku, como desejado. Pode ficar.
- **`Explore.md`:** correto. `name: Explore` substitui o embutido, `model: haiku` vale e `omitClaudeMd` é campo válido. Sem mudança.
- **`change-reviewer`, `postgres-dba`, `security-reviewer`:** `disallowedTools: Write, Edit` deixa o Bash livre, ou seja, pode editar via shell, rodar `psql` ou ler `.env`. Texto novo do frontmatter:
  `disallowedTools: Write, Edit, NotebookEdit` e, no corpo, "Bash só para `git diff`, `git log`, `git show`, `pytest` e `ruff`/`mypy` em modo leitura; nunca redirecione saída para arquivo nem rode `psql`, `alembic upgrade` ou `rm`".
  No `postgres-dba`, trocar o Bash por `tools: Read, Grep, Glob` (ele analisa migrações, não precisa executar).
- **`~/.claude/settings.json` (global):** consertar o JSON e tirar o `effort max` (C3). Pede confirmação.
- **Skill `economia-de-tokens`:** as afirmações batem com a doc. Ajustes:
  - §1, linha "Mudanças no CLAUDE.md": → "Mudanças no `CLAUDE.md` raiz só valem após `/clear`, `/compact` ou reinício."
  - §2 Esforço, acrescentar: "`CLAUDE_CODE_EFFORT_LEVEL` em settings sobrepõe `/effort`; não defina essa variável. Padrão do projeto: `medium`."
  - §1, nova linha: "Pausas longas e previsíveis: cache de 1 h (`promptCacheTtl: \"1h\"`) custa mais para gravar; só vale se você volta à mesma sessão em menos de 1 h com frequência. Padrão: não usar."
  - §3, acrescentar: "Meça na 1ª semana com `/usage`. Se a projeção passar de US$ 50/mês, avalie a assinatura Claude (Pro/Max) em vez da API (D-30)."

## 4. Claude Code + OpenCode
**Decisão: só Claude Code, a partir de agora.** O OpenCode Go fica parado até vencer (≤ 2 semanas) e não é renovado.
**Motivos:**
1. As falhas relatadas (lentidão, baixa qualidade) e a 003H (timeouts de 300 s no `build`) foram no executor, justamente o papel crítico.
2. Os revisores do OpenCode tinham `read: deny` e recebiam só texto colado, sem poder conferir o código. Isso é revisão cega.
3. Duas fontes de regras: com `AGENTS.md` presente, o OpenCode **ignora o `CLAUDE.md`** (doc opencode.ai/docs/rules), e o Claude Code ignora o `AGENTS.md` quando há `CLAUDE.md`. Hoje cada ferramenta segue um documento diferente, e o `AGENTS.md` manda ler o plano inteiro, contra o `CLAUDE.md`.
4. Coordenar duas ferramentas custa tempo e tokens (repassar contexto, reconciliar relatórios: 003D, 003F e 003H ainda pendentes), o que pesa para um dev solo com 25 h/semana.
5. Com cache, Haiku no `Explore` e Sonnet no resto dentro de uma única sessão saem mais baratos e previsíveis que reenviar contexto entre ferramentas.
6. O plugin de fallback reenvia prompts a outros provedores, um risco de privacidade ainda não decidido.

**Critérios para rever a decisão:** (a) gasto real com Claude Code > US$ 50/mês por 2 meses, mesmo seguindo a skill e já tendo avaliado a assinatura; (b) Sonnet falha 2× na mesma tarefa com contexto limpo, em mais de uma tarefa por mês; (c) surge no OpenCode um modelo de qualidade comprovada, mais barato, para tarefas mecânicas.

**Protocolo mínimo, se um dia voltar:** OpenCode só em `git worktree` ou branch próprios, nunca no mesmo diretório ao mesmo tempo. `opencode.json` com `"instructions": ["CLAUDE.md"]` e sem `AGENTS.md` (uma fonte só). Papel só de executor mecânico ou de 2ª opinião somente leitura com acesso de leitura ao código. A passagem de trabalho é só por `docs/tasks/NNN` (entrada) e `docs/reviews/NNN` (saída). A RETOMADA é atualizada apenas pela sessão Claude. Plugin de fallback desligado.

**Limpeza (pede aprovação, apaga arquivos):** depois do vencimento, um commit que arquiva ou remove `.opencode/`, `opencode.json*`, `prompts/`, `AGENTS.md` e `CLAUDE.old.md`, e encerra 003D, 003F e 003H como "descontinuadas".

## 5. Decisões do Fagner (novas)
| ID | Decisão | Sugestão |
|---|---|---|
| D-27 | Reembolso, estorno e MED do Pix: quem pode, efeito na liberação | Só o fotógrafo inicia; recálculo + revogação de links |
| D-28 | Cliente sem e-mail | Link copiável pelo fotógrafo (WhatsApp manual) |
| D-29 | Editor que estoura o prazo | Aviso ao dono por e-mail; sem multa automática no B1 |
| D-30 | Cobrança do Claude: API ou assinatura; teto US$ 50 | Medir 1 semana e decidir |
| D-31 | Aposentar o OpenCode e remover os arquivos | Sim, após o vencimento |
| D-32 | Lookup pré-contexto sob RLS (C2) | Funções `SECURITY DEFINER` mínimas |

## 6. Próximos 3 passos
1. **Settings** (minutos, com sua confirmação): consertar o JSON global e tirar o `effort max`; acrescentar o deny de Bash/PowerShell e o `ask` de push no projeto; ajustar o frontmatter dos 3 revisores.
2. **Tarefa 005C, alinhamento de documentos** (Sonnet, só docs): roadmap com 005B e a quebra de 007/012/016; §10 com `refunds`, campos de retenção e classificação de `webhook_events`; D-27 a D-32; RETOMADA enxuta; linha de checks do `CLAUDE.md`; skill ajustada; ADR-007 em proposta.
3. **005B revisada** (Sonnet + `postgres-dba`): incluir C2 (lookup pré-contexto), aprovar e implementar. Depois disso, a Etapa 0 fecha e começa a 006.

## 7. Aplicado em 03/11/2026 (autorizado pelo Fagner: plano, CLAUDE.md, agentes)
- `docs/PLANO-MESTRE.md` → v3.1: C1 (005/005B no roadmap e no status), C2 (§8 regra 8, classificação no §10, S-40), A1/A2 (§4.2 cancelamento, §4.3 estorno, §4.7, `refunds`, S-41), A3 (007a/b, 012a/b, 016a/b), A4 (plano padrão semeado, Mailpit na 009, D-03 antes da 021), A5 (campos de retenção, recontagem de `studio_usage`), A6 (ordem das ADRs), M1–M9, D-27 a D-32, riscos novos, §15 com ferramenta única.
- `CLAUDE.md`: ferramenta única, checks reais, regra de pré-contexto, estorno, `.env` por qualquer ferramenta, commit só dos arquivos da tarefa, esforço `medium`.
- `.claude/agents/`: `change-reviewer` e `security-reviewer` com `NotebookEdit` bloqueado e Bash restrito a leitura; `postgres-dba` com `tools: Read, Grep, Glob` e checagens de RLS forçada e `SECURITY DEFINER`. `Explore` sem mudança.
- `docs/RETOMADA.md` reescrita; o histórico foi para `docs/reviews/historico-retomada-ate-2026-11-02.md`.
- **Não aplicado** (fora do pedido): `~/.claude/settings.json`, `.claude/settings.json`, skill `economia-de-tokens`, remoção dos arquivos do OpenCode (D-31).

> Fagner: ao terminar de ler, rode `/clear` e depois `/model sonnet`.
