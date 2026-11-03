---
name: economia-de-tokens
description: Diz quando dar /clear, /compact ou /rewind e qual modelo usar (Haiku, Sonnet ou Opus) para gastar menos tokens. Use sempre que uma tarefa terminar ou for começar, quando o assunto mudar, depois de debug longo ou muitos logs, quando a sessão estiver pesada, e quando a pessoa perguntar "devo dar /clear?", "qual modelo?", "posso usar Opus?" ou reclamar de gasto de tokens.
---

# Economia de tokens (Claude Code + API)

Por que importa: a cada passo o Claude Code reenvia **todo** o contexto. Contexto velho custa em toda mensagem. O cache de prompt, com chave de API, dura 5 minutos por padrão; depois de uma pausa maior a próxima mensagem reprocessa tudo sem desconto.

Quem digita `/clear`, `/compact` e `/model` é o Fagner. Quando perceber um sinal abaixo, diga **em uma linha** o que sugere e por quê, e deixe pronto um resumo de 3 a 5 linhas (tarefa, estado, próximo passo) para colar na sessão nova. Não dê sermão.

## 1. Quando dar /clear, /compact ou /rewind

| Situação | Ação |
|---|---|
| Tarefa concluída e commitada, vai começar outra | `/clear`. Antes, atualize `docs/RETOMADA.md` |
| Mudou de assunto (backend → frontend, B1 → álbuns) | `/clear` |
| Debug longo, erro repetido ou logs grandes no contexto | `/clear` e recomece com o resumo do que já se sabe |
| Voltou de uma pausa de mais de 5 minutos e a próxima tarefa é outra | `/clear` (continuar custa reler tudo sem cache) |
| Mesma tarefa, contexto útil mas grande (confira com `/context`) | `/compact` com instruções. Faça em pausa natural, com o cache ainda quente |
| Seguiu por um caminho errado dentro da mesma tarefa | `Esc` e `/rewind`. Mantém o cache e descarta o desvio |
| Dúvida rápida sem relação com a tarefa | `/btw` (não entra no histórico) |
| Precisa voltar depois a uma conversa | `/rename nome` antes do `/clear`; depois `/resume` |

Evite: `/compact` depois de uma pausa longa (é uma requisição enorme sem cache), `/compact` logo antes de um `/clear`, e deixar uma sessão aberta o dia todo. **Uma tarefa = uma sessão.**
Mudanças no `CLAUDE.md` só valem a partir do próximo `/clear` ou reinício.

## 2. Qual modelo usar

Comece no mais barato que resolve. Suba só se falhar.

| Modelo | Use para | Nunca para |
|---|---|---|
| **Haiku** (`haiku`) | Buscar e ler código, listar usos, resumir arquivo ou log, rodar testes e relatar só as falhas, mensagem de commit, renomear e formatar, boilerplate de um arquivo, conferir checklist. Via subagente `Explore` | Auth, pagamento, RLS, migrações, decisões de arquitetura |
| **Sonnet** (`sonnet`) — **padrão** | Implementar a tarefa, escrever testes e migrações, depurar, revisar diff, planejar tarefas normais (modo plan), escrever especificação de tarefa, subagentes revisores | Nada é proibido; só não gaste Opus onde Sonnet resolve |
| **Opus** (`opus`) — **último caso** | **Somente planejar algo complexo** (abaixo) | Escrever código rotineiro, revisar, depurar, ler código |

### Quando o Opus é permitido (precisa de aprovação do Fagner)
Só se **um** destes for verdadeiro:
- (a) O desenho cruza vários módulos e é difícil de desfazer. Exemplos do projeto: modelo de dados multi-tenant com RLS, fluxo de pagamento com split, matriz de liberação, sequência do álbum com versões.
- (b) O Sonnet tentou duas vezes uma decisão de design, com contexto limpo, e não resolveu.
- (c) Há requisitos em conflito sem saída óbvia.

### Protocolo do Opus
1. Peça aprovação em uma frase: "Quero usar Opus para X porque (a/b/c)."
2. `/clear` antes. Trocar de modelo no meio da conversa perde o cache e relê tudo sem desconto.
3. `/model opus`. Leve **contexto mínimo**: a tarefa, as seções do plano que importam e uma pergunta fechada.
4. A saída é um **documento curto** (`docs/adr/` ou `docs/tasks/`) com decisão, motivo e passos. Não implemente na sessão do Opus.
5. `/clear`, `/model sonnet` e implemente.

Não use `opusplan`: ele troca de modelo a cada entrada e saída do modo plan e perde o cache toda vez.

### Esforço (`/effort`)
No Haiku, Sonnet e Opus 5.5, com chave de API, trocar o esforço mantém o cache. `low` para tarefa mecânica, `medium` no dia a dia, `high` só ao planejar algo complexo. Evite `xhigh` e `max`. O raciocínio estendido não pode ser desligado nesses modelos; o esforço é a alavanca.

## 3. Hábitos que economizam

- **Prompt específico:** diga arquivo, função e critério de aceite ("`pytest tests/isolation/test_galleries.py` deve passar"). Use `@caminho` em vez de pedir para procurar.
- **Plano por seção:** leia só o que a tarefa lista em "Ler:". Nunca o `PLANO-MESTRE` inteiro.
- **Plan mode** (Shift+Tab) antes de mexer em esquema, segurança ou mais de 3 arquivos. Evita refazer.
- **Saída volumosa para subagente:** testes, logs, busca larga e leitura de documentação. Só o resumo volta.
- **Filtre antes de colar:** `| tail -50`, `grep`, só as falhas.
- **Teste em incrementos:** um arquivo, roda, segue.
- **Interrompa cedo:** `Esc` assim que ele ler o que não devia ou for pelo caminho errado.
- **Medir:** `/context` mostra o que pesa; `/usage` mostra custo e acerto de cache.
- **MCPs:** desligue os que não está usando (`/mcp`); prefira CLI (`git`, `gh`) a MCP.
- **CLAUDE.md curto** (menos de 200 linhas). Instrução de fluxo específico vai para skill.

## 4. Como Claude deve se comportar

- Só fale de tokens, `/clear` ou modelo quando houver um sinal das seções 1 ou 2. Uma linha, no fim da resposta.
- Tarefa de nível Haiku (buscar, resumir, formatar) em sessão grande: delegue ao `Explore` em vez de ler os arquivos no contexto principal.
- Pedido de arquitetura complexa: faça primeiro a proposta em modo plan com Sonnet. Só sugira Opus se (a), (b) ou (c) valer, e **nunca troque de modelo sozinho**.
- Não repita o conselho se o Fagner já o recusou nesta sessão.
