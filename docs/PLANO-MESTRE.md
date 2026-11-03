# PLANO MESTRE v3 — Pics (plataforma para fotógrafos)

> Fonte da verdade de escopo, arquitetura e regras. Dono do produto e decisor final: **Fagner**. Versão 3.1 — 03/11/2026 (correções da `docs/reviews/revisao-opus-001.md` sobre a v3 de 02/11/2026). Substitui a v2.
> **Não leia o documento inteiro.** Use o mapa de leitura (§0.2) e leia só as seções da tarefa.
> Status vivo das tarefas: `docs/RETOMADA.md`. Este plano só registra a ordem e o escopo.

---

## 0. Como usar este documento

### 0.1 Regras para agentes
1. Leia `CLAUDE.md` e a tarefa `docs/tasks/NNN-nome.md`. Da tarefa, leia só as seções do plano que ela lista em "Ler:".
2. Uma tarefa por vez. O que estiver fora do escopo vai para `docs/reviews/` como observação, sem correção por conta própria.
3. Tudo marcado **REQUER APROVAÇÃO** (§17 e `CLAUDE.md`) só avança com aprovação explícita do Fagner.
4. Dados fictícios. Nunca coloque fotos reais, dados de clientes, chaves ou `.env` em prompts, logs, testes ou commits.
5. `git commit` antes e depois de cada tarefa. No máximo 2 rodadas de correção; depois pare e consulte.
6. Antes de instalar qualquer pacote, confirme que o nome existe e é o oficial. Dependência nova **REQUER APROVAÇÃO**.
7. **Toda tabela de negócio tem `studio_id`** e toda consulta respeita o estúdio (§8). Nunca é opcional.
8. Skills e MCPs: só os que a tarefa listar (§15).

### 0.2 Mapa de leitura (o que ler por tipo de tarefa)

| Tarefa | Ler |
|---|---|
| 003–005 Fundação | §7, §8, §9, §10 (plataforma), §13 (S-xx da tarefa) |
| 005B Multi-tenant e RLS | §8 (regras 1 a 3 e 8), §10 (plataforma e "Classificação das tabelas"), §13 (S-27, S-40) |
| 006–009 Identidade e acesso | §3, §8 (regra 8), §13 (inclui S-40), §14 (L-03) |
| 010–011 Storage e imagens | §11, §12, §13 |
| 012–015 Clientes, pacotes, galerias, seleção | §4.1 a §4.4, §4.8, §4.9, §10 (B1), §11 |
| 016–019 Pagamento, liberação, edição, entrega | §4.2 a §4.7, §10 (B1), §11, §13 (inclui S-40, S-41) |
| 020 Planos e assinatura | §12, §17 (D-12 a D-14) |
| 021–022 Pré-beta e beta | §13, §14, §15, §18 |
| 023–027 Álbuns | §5, §10 (B2) |
| 028+ Gestão e site | §6 |
| 039–041 Lançamento | §13, §14, §18 |

### 0.3 O que mudou da v2 para a v3 (conflitos entre os documentos e como foram resolvidos)

| Tema | Decisão na v3 |
|---|---|
| Ordem dos blocos | **B1 Entrega → B2 Álbuns → B3 Gestão do estúdio e site** (definida pelo Fagner em 02/11/2026). Na v2 a gestão vinha antes dos álbuns. Os blocos foram renumerados |
| Nome das fases | O roadmap usa **Etapas** (0 a 6). "Fase 1/2/3" do plano de negócio e do PDF não se usam mais |
| Pacotes A, B, C, D, estados e matriz de liberação | Entram no B1 como regra de negócio (§4). Vêm do plano de negócio de 02/11/2026 |
| Escopo do B1 | Passa a incluir edição mínima, pacote de entrega (ZIP) e retenção. Na v2 só havia prévia, pagamento e download |
| Formato das prévias | WebP com marca d'água. AVIF é opcional, depois de validar suporte (nova dependência exige aprovação). A v2 dizia JPEG |
| Diagramação do álbum | **Manual, em software externo** (PDF e plano de negócio). O sistema não terá editor de lâminas. A v2 previa montagem e ilustração de lâminas no app. Vídeo de diagramação (PDF) fica fora. Confirmar em D-23 |
| Fila de edição, atribuição a editores e SLA | Saem do B1 e vão para o B3 (tarefa 036). No B1 o próprio fotógrafo pode ser o editor |
| Google Drive (pacote B) | Canal de entrega opcional, depois do MVP |
| Revisão de segurança "por modelo diferente" (v2) | Trocada por revisão em contexto limpo (subagente) mais ferramentas automáticas (S-26). Só há modelos Claude |
| Decisões pendentes | As 7 do plano de negócio foram fundidas à lista da v2 (§17) |

**v3.1 (03/11/2026, `docs/reviews/revisao-opus-001.md`):** 005B entra no roadmap (RLS saiu da 005); resolução de estúdio antes do contexto RLS (§8 regra 8, S-40); reembolso, estorno e MED do Pix (§4.7, `refunds`, S-41); campos de retenção (§10); formatos, duplicatas e abuso (§11); tarefas 007, 012 e 016 divididas; dependências 009, 010 e 015 ajustadas; decisões D-27 a D-32; ferramenta única: Claude Code (OpenCode descontinuado, D-31).

---

## 1. Visão do produto

Plataforma web (SaaS) para fotógrafos e estúdios entregarem e gerenciarem seu trabalho. Cada fotógrafo (um **estúdio**) tem seu espaço, sua marca, seus clientes e suas galerias.

### Os três blocos, na ordem de entrega

| Bloco | Conteúdo | Meta |
|---|---|---|
| **B1 — Entrega de fotos** | Galerias com prévias, favoritos, seleção, pacotes A/B/C, pagamento Pix (sinal e saldo), edição mínima, download de originais e do pacote de entrega, e-mails, planos e cotas | **MVP**: uso real por 3 a 5 fotógrafos |
| **B2 — Álbuns** (Pacote D) | Seleção das fotos do álbum pelo cliente, **sequência** das fotos, tamanho, ilustração, prova e aprovação, exportação para quem diagrama | Depois do B1 estável |
| **B3 — Gestão do estúdio e site** | Site personalizado por fotógrafo (gerado automaticamente ao contratar), CRM, agenda, contratos, briefing, e-mail/WhatsApp, financeiro, fila de edição, métricas | Detalhado a partir do que o beta pedir |

### Restrições
- **Custo baixo**: infraestrutura barata, sem custo de saída de dados.
- **Segurança forte**, com **isolamento entre estúdios** como risco nº 1 (§13).
- **LGPD desde o projeto**: o fotógrafo é o controlador e a plataforma é a operadora (§14).
- **Visual extraordinário** no site e nas áreas logadas (B3).
- Desenvolvimento assistido por IA: tarefas pequenas, revisáveis, com critérios de aceite claros.

---

## 2. Referência competitiva (Davions, consultado em 02/11/2026)

> Referência de **funcionalidades e preços**. Não copiar textos, layout, identidade visual nem código. Confirmar no site deles antes de decidir preços.

- Todos os planos: kanban, CRM, agendamento online, contratos, questionários, e-mails/WhatsApp, galeria de provas e de entrega, integração com Lightroom, site com SEO, financeiro.
- "Em breve" no site deles: diagramador de álbuns (limites mensais por plano), blog e posts com IA, loja integrada, e-mail marketing.
- Planos: Standard R$ 149/mês (100 GB, sem equipe), Pro R$ 299 (500 GB, até 5 membros), Ultimate R$ 449 (1.000 GB, multi agenda, equipe ilimitada). Teste grátis de 30 dias sem cartão.
- Lições: armazenamento é o eixo dos planos e o maior custo variável (§12); equipe com permissões é recurso de plano; trial sem cartão atrai abuso; o diferencial do B2 (álbuns) precisa ser validado com fotógrafos reais.

---

## 3. Atores

| Ator | Descrição |
|---|---|
| `platform_admin` | Fagner e equipe da plataforma: estúdios, planos, suporte |
| `studio_owner` | O fotógrafo. Gerencia tudo do próprio estúdio |
| `studio_member` | Equipe, com permissões configuráveis. **Editor** é uma permissão (`deliver_edits`) de `studio_member`; no B1 o dono pode ser o editor |
| `assembler` | Diagramador do álbum (interno ou convidado externo, B2) |
| `client` | Cliente do fotógrafo: vê galerias, seleciona, paga, baixa |
| Visitante | Navega no site do estúdio (B3) |

---

## 4. B1 — Entrega de fotos: regras de negócio

### 4.1 Pacotes

| Pacote | O cliente contrata | Seleção | Cobrança extra | Liberação |
|---|---|---|---|---|
| **A** Fotos brutas, sem edição | Todas as fotos sem tratamento | Nenhuma | Edição opcional de fotos escolhidas, por foto (valor em D-20) | Originais na hora, com o evento QUITADO. Editadas, quando o editor entregar |
| **B** Todas as fotos + cota de editadas | Todas as fotos e N editadas | Escolhe as editadas, até a cota | Valor por foto acima da cota, pago antes de entrar na fila | Originais com o evento QUITADO. Editadas, quando o editor entregar, dentro do prazo |
| **C** Pacote fixo de editadas | Quantidade fixa (ex.: 20) | Escolhe, entre todas, a quantidade contratada | Cada foto acima da quantidade é adicional, paga antes de entrar na fila | Só quando o editor entregar |
| **D** Álbum | Álbum com sequência e diagramação | Cliente escolhe as fotos e a ordem | Valor em D-25 | Depois da aprovação da prova. **É o B2 (§5)** |

- O pacote A com edição extra usa a mesma rodada de edição dos pacotes B e C.
- O sistema calcula sozinho o acréscimo quando a seleção passa da cota e cria um pedido de adicional. A foto extra só entra na fila de edição depois do pagamento.

### 4.2 Estados (dois estados independentes por evento)

- **Financeiro** (`events.financial_status`): PENDENTE (`pending`), PARCIAL (`partial`, ex.: sinal de 50%), QUITADO (`paid`). Sempre **calculado dos pagamentos confirmados**.
- **Galeria** (`galleries.status`): `draft` (rascunho) → `published` → `selection_closed` → `in_editing` → `ready` → `delivered`; e `expired`.
- Caminhos por pacote:
  - **A**: `published` → `ready` quando QUITADO (originais liberados) → `delivered` no 1º download. Com edição extra, segue o caminho de B/C.
  - **B**: `published` → `selection_closed` → `in_editing` (se houver editadas) → `ready` → `delivered`. Os originais liberam com QUITADO, independente da edição.
  - **C**: `published` → `selection_closed` → `in_editing` → `ready` → `delivered`. Sem download de originais.
- A seleção termina quando o cliente confirma ou quando o prazo das prévias acaba (`selection_closed`).
- **Cancelamento** do evento (`events.canceled_at`) só pelo fotógrafo: bloqueia novos pedidos e downloads, cancela pedidos pendentes e segue a retenção. Saldo não pago no prazo: regra em D-18.
- O fotógrafo decide se reabre uma galeria encerrada. A reabertura gera as prévias de novo a partir dos originais, enquanto eles existirem (cobrança em D-19).
- Transições são validadas **no servidor**.

### 4.3 Matriz de liberação (regra de negócio mais sensível do B1)

| Ação do cliente | PENDENTE | PARCIAL | QUITADO |
|---|---|---|---|
| Ver prévias e favoritar | Sim | Sim | Sim |
| Confirmar seleção | Não (sugerido; confirmar em D-22) | Sim | Sim |
| Início do prazo de edição | Não | Sim, com o sinal pago | Sim |
| Baixar originais (pacotes A e B) | Não | Não | Sim |
| Baixar editadas e pacote de entrega | Não | Não | Sim |

A liberação depende do pacote, do estado financeiro e do estado da edição. É checada **no servidor a cada pedido de download** (S-35), nunca só na tela.
**Estorno ou cancelamento:** o estado financeiro é recalculado; se deixar de ser QUITADO, `release.py` volta a negar e os links de entrega ativos são revogados (S-41). Evento cancelado nega todas as linhas, exceto ver prévias enquanto existirem.

### 4.4 Fluxo ponta a ponta
1. O fotógrafo cria cliente, evento (com pacote e prazos) e galeria, e faz upload em lote. O sistema gera as prévias.
2. O fotógrafo publica. O cliente recebe o acesso por e-mail (ou, sem e-mail, o fotógrafo copia o link e envia por conta própria, D-28) e o prazo das prévias começa (sugerido: 3 dias).
3. O cliente navega, favorita e seleciona conforme o pacote.
4. O cliente paga por Pix. O sinal (PARCIAL) permite confirmar a seleção e iniciar a edição; o download fica bloqueado até o saldo.
5. A seleção termina (confirmação ou prazo). Galeria em `selection_closed`; prévias apagadas (§4.6).
6. Se houver edição, vai para `in_editing`. O editor sobe as editadas na área de entrega dentro do prazo.
7. Os arquivos finais ficam na área de entrega. O sistema gera o ZIP em segundo plano e cria um link assinado de curta duração, renovável.
8. O cliente recebe o link por e-mail e também baixa pelo site. Cada download é registrado.
9. Prévias, pacote de entrega e originais expiram conforme §4.6.

### 4.5 Edição (mínimo do B1)
- Status por foto: `selected`, `in_editing`, `edited`.
- Prazo de edição por galeria, customizável. Sugerido: começa quando a seleção encerra e o sinal (ou o adicional) está confirmado.
- O editor (ou o dono) sobe as editadas na área de entrega. Fila, atribuição a editores e SLA ficam no B3 (036).
- Prazo de edição vencido: o dono recebe aviso por e-mail; sem multa nem ação automática no B1 (D-29).

### 4.5.1 Notificações do B1 (só e-mail)
Cliente: acesso, lembrete de prévias, pagamento confirmado, entrega. Fotógrafo: seleção confirmada, pagamento recebido ou estornado, prazo de edição vencendo, ZIP com falha.

### 4.6 Retenção e armazenamento (valores sugeridos, configuráveis; confirmar em D-07 e D-22)

| Arquivo | Criado | Apagado |
|---|---|---|
| Prévias | Ao publicar | Quando a seleção encerra, exceto em reabertura |
| Originais | No upload | 60 dias depois da entrega (cobre reabertura e saldo pendente) |
| Pacote de entrega (editadas e ZIP) | Quando os arquivos finais são enviados | 30 dias depois da entrega, renovável pelo fotógrafo |

- A cota do plano conta só os arquivos existentes no momento e cai quando eles expiram.
- A expiração usa regras de ciclo de vida do storage e rotina agendada (MinIO no dev; R2 ou B2 em produção).
- Os prazos aparecem para o cliente no e-mail e na galeria.

### 4.7 Pagamento
- Pix, com sinal parcial e saldo, e cobrança de adicionais antes da edição.
- **A confirmação vem só do webhook do provedor**, nunca de ação do cliente. Webhook assinado, validado e idempotente; cada pagamento registrado para conciliação.
- Dinheiro do cliente final não fica retido na plataforma (subconta/split, D-01).
- **Reembolso, estorno e MED** (Mecanismo Especial de Devolução do Pix): só o fotógrafo inicia o reembolso; devoluções chegam por webhook e viram `refunds`. Cada uma recalcula `financial_status` e aplica a regra de estorno da §4.3. Regras de quem pode e de reembolso parcial em D-27.

### 4.8 Configuração por pacote (o fotógrafo define)
Preço, cota de editadas, valor da foto extra, percentual do sinal (sugerido 50%), prazo das prévias (sugerido 3 dias), prazo de edição, validade do link de entrega (sugerido 30 dias). Ao contratar, os valores são copiados para o evento (`events.terms`), para que mudar o pacote depois não altere eventos já fechados.

### 4.9 UX da galeria do cliente
Mobile first. Prévias leves com lazy loading. Filtros: todas, favoritas, selecionadas (cliente e painel do fotógrafo). Micro-animações ao favoritar e selecionar, transição suave entre fotos e **modo slideshow**. Tudo respeitando `prefers-reduced-motion`. Marca do estúdio (logo e cores).

---

## 5. B2 — Álbuns (Pacote D): regras de negócio

**Escopo decidido (confirmar em D-23):** a diagramação das lâminas é **manual, feita pelo estúdio em software externo**. O sistema não é editor de lâminas.

O sistema cuida de:
1. **Seleção das fotos** do álbum pelo cliente, a partir da galeria do evento.
2. **Sequência**: o cliente define a ordem. Sugestão inicial automática por horário da foto (`taken_at`); depois reordena arrastando (no celular, com toque longo ou setas). Ordem cronológica ou narrativa, à escolha do cliente. Comentário opcional por foto.
3. **Tamanho e páginas**: o cliente escolhe entre os tamanhos do estúdio, respeitando mínimo e máximo de páginas (D-06).
4. **Ilustração**: visualização folheável do álbum. Antes da diagramação mostra a sequência no formato escolhido; na prova mostra as lâminas enviadas pelo estúdio (D-24).
5. **Prova e aprovação**: o estúdio sobe as imagens das lâminas prontas; o cliente comenta por lâmina, pede ajustes ou aprova. Cada rodada é uma versão; a aprovação é registrada no `audit_log`.
6. **Exportação** para quem diagrama: ZIP numerado na ordem final mais manifesto (CSV e PDF de conferência).
7. **Diagramador convidado**: link com acesso restrito a um único álbum, com validade.

**Estados do álbum:** `draft` → `selecting` → `sequencing` → `submitted` (cliente confirmou; sequência travada com número de versão) → `in_assembly` → `proof_sent` ⇄ `changes_requested` → `approved` → `delivered`. Transições validadas no servidor.

Liberação do álbum final e cobrança: D-25. Diferencial a validar com fotógrafos reais (hipóteses): fluxo pensado para o diagramador externo, simplicidade, preço e Pix. O concorrente anuncia um diagramador como "em breve".

---

## 6. B3 — Gestão do estúdio e site (épicos; detalhar depois do beta)

- **Site do estúdio**: gerado automaticamente com padrão personalizável quando o fotógrafo contrata o plano; páginas, tema, portfólio, contato, blog; subdomínio e depois domínio próprio; SEO.
- **CRM e Kanban**; cadastro central de clientes, histórico de ensaios, status das galerias, histórico de aprovações e downloads.
- **Agenda e agendamento online**.
- **Contratos** gerados a partir do pacote e assinatura eletrônica (D-17).
- **Briefing e questionários**.
- **E-mails e WhatsApp automatizados** (D-16).
- **Financeiro e dashboard**: receitas, pendentes, parciais e quitados, previsão de recebimentos via Pix, faturamento por evento, despesas, relatórios.
- **Fila de edição**: atribuição de eventos a editores, controle de prazos e monitoramento de SLA.
- **Métricas**: conversão de fotos extras além da cota e consumo de storage por cliente e plano.
- Marketing (posts, campanhas): avaliar depois.

---

## 7. Requisitos não funcionais

- **Segurança**: §13. **LGPD**: §14. **Isolamento entre estúdios**: nenhum estúdio acessa dado, foto ou arquivo de outro.
- **Desempenho**: upload direto ao storage; processamento e ZIP em segundo plano; prévias leves; miniaturas; paginação.
- **Mobile first** (o cliente escolhe pelo celular). **Acessibilidade** WCAG AA (contraste, teclado, `prefers-reduced-motion`).
- **Idioma** pt-BR. Datas em UTC no banco. **Dinheiro sempre em centavos** (inteiro).
- **Observabilidade**: logs estruturados com `request_id` e `studio_id`, sem dados pessoais nem segredos.
- **Custo**: medir armazenamento por estúdio e impor cotas.

---

## 8. Arquitetura (multi-tenant)

```
Navegador ──► Frontend (Next 16) ──► API (FastAPI) ──► PostgreSQL (RLS)
                                        │
                                        ├──► Storage S3-compatível PRIVADO (prefixo por estúdio)
                                        ├──► Worker em segundo plano (derivados, marca d'água, ZIP, expiração)
                                        ├──► E-mail transacional
                                        └──► Provedor de Pix com subcontas/split (webhook assinado)
```

| Camada | Escolha |
|---|---|
| Backend | Python 3.12 ou 3.13, FastAPI, Pydantic v2, pydantic-settings |
| Banco | PostgreSQL, SQLAlchemy 2, Alembic |
| Auth | Sessão opaca no servidor + cookie `HttpOnly`; argon2id; 2FA TOTP para dono e admin |
| Imagens | Pillow (ou pyvips), em worker |
| Storage | S3-compatível privado (Cloudflare R2 ou Backblaze B2; MinIO no dev) via boto3 e URLs assinadas |
| Frontend | Next 16, TypeScript estrito, Tailwind; shadcn/ui **REQUER APROVAÇÃO** |
| Qualidade | ruff, mypy, pytest, ESLint, `tsc`, CI no GitHub Actions |
| Infra local | Docker Compose (WSL 2): PostgreSQL, MinIO, Mailpit |

### Regras de multi-tenancy (obrigatórias)
1. **Estúdio = tenant.** Toda tabela de negócio tem `studio_id NOT NULL`, indexado.
2. **Chaves estrangeiras compostas** com `studio_id` onde fizer sentido.
3. **RLS no PostgreSQL** como segunda barreira (`SET LOCAL app.studio_id`); o papel do banco da API **não tem `BYPASSRLS`**. A checagem na aplicação continua obrigatória.
4. **Testes de isolamento**: para cada rota, dois estúdios; A não lê, altera nem apaga dados de B (401/403/404).
5. **Storage**: chaves `studios/{studio_id}/...`; URL assinada só depois de checar permissão e estúdio.
6. **Acesso de suporte** da plataforma a dados de estúdio: restrito, justificado e registrado no `audit_log`.
7. **Sites dos estúdios** (B3) em **domínio separado** do app.
8. **Resolução do estúdio antes do contexto RLS** (S-40). Três fluxos chegam sem `studio_id`: link do cliente final, webhook do provedor e login de usuário com vários estúdios. Eles usam **funções `SECURITY DEFINER` mínimas** (proposta, decisão em D-32), por exemplo `resolve_client_token(token_hash) → (studio_id, gallery_id)` e `resolve_payment_ref(provider, provider_ref) → studio_id`. Essas funções têm dono sem login, `search_path` fixo, retornam só identificadores e têm teste próprio. Depois a API faz `SET LOCAL app.studio_id` e segue com RLS normal. Proibido contornar com papel `BYPASSRLS` ou com consulta sem filtro.

### Frontend e backend
Em produção, `app.dominio` e `api.dominio`, cookie `SameSite=Lax`, `Secure`, `HttpOnly`. Ações que alteram dados exigem proteção CSRF (token por sessão + `Origin`). CORS com origens explícitas vindas do `.env`, nunca `*` com credenciais.

### ADRs a registrar em `docs/adr/` (status: proposta até aprovação)
001 Frontend e backend separados · 002 PostgreSQL + SQLAlchemy 2 + Alembic · 003 Sessão opaca com cookie `HttpOnly` · 004 Storage privado com URLs assinadas · 005 Imagens e ZIP em worker com limites · 006 Dinheiro em centavos e webhooks idempotentes · 007 Multi-tenancy com `studio_id` + RLS (inclui a regra 8) · 008 Domínio separado para sites dos estúdios · 009 Matriz de liberação decidida no servidor.
Existem ADR-001 a ADR-006 (proposta). **A ADR-007 precisa estar aprovada antes de implementar a tarefa 005B**; a ADR-008 antes da tarefa 029; a ADR-009 antes da tarefa 017.

---

## 9. Estrutura alvo

```
backend/app/
├─ main.py
├─ api/v1/{router.py, deps.py, routes/{health,auth,studios,clients,packages,events,galleries,photos,selections,orders,billing,webhooks,delivery,albums}.py}
├─ core/{config.py, security.py, logging.py, tenancy.py}
├─ db/{base.py, session.py}   models/  schemas/  repositories/
├─ services/{storage.py, images.py, mail.py, payments.py, quotas.py, release.py, delivery.py}
└─ workers/{process_photo.py, build_delivery_zip.py, expire_files.py}
backend/{alembic/, tests/{unit,integration,isolation}/, pyproject.toml, requirements*.txt, .env.example}
frontend/src/{app/, components/{ui,layout}, lib/, hooks/, types/, services/}
infra/docker-compose.yml   docs/{adr/, tasks/, reviews/, lgpd/, RETOMADA.md}
.claude/{agents/, skills/, settings.json}   .github/workflows/ci.yml   .github/dependabot.yml
```
`services/release.py` concentra a **matriz de liberação** (§4.3). Rotas de download passam por ele; nenhuma rota decide sozinha.

---

## 10. Modelo de dados (proposta; o `postgres-dba` valida antes da migração)

PostgreSQL, chaves `uuid`, `timestamptz` (UTC), dinheiro em centavos. **Toda tabela de negócio tem `studio_id`.**

### Classificação das tabelas (validar na 005B)
- **Globais** (sem `studio_id`, sem RLS de estúdio, sem dado de cliente final): `users`, `sessions`, `plans`, `webhook_events` (só `payload_hash`, sem payload nem PII).
- **Mista:** `audit_log` (`studio_id` nulo só para eventos da plataforma).
- **Tenant** (`studio_id NOT NULL` + RLS): todas as demais.
- Acesso pré-contexto às tabelas tenant: só pelas funções da §8 regra 8.

### Plataforma e estúdio
| Tabela | Campos principais |
|---|---|
| `studios` | id, name, slug (único, validado, nomes reservados), status, plan_id, created_at |
| `users` | id, email (citext único), password_hash, platform_role, full_name, is_active, totp_secret (criptografado) |
| `studio_members` | studio_id, user_id, role (`studio_owner`/`studio_member`/`assembler`), permissions (jsonb) |
| `plans` | id, name, price_cents, storage_gb, max_members, albums_per_month, features (jsonb), active |
| `subscriptions` | id, studio_id, plan_id, status (`trial`/`active`/`past_due`/`canceled`), trial_ends_at, current_period_end, provider_ref |
| `studio_usage` | studio_id, bytes_used, photos_count, updated_at |
| `studio_branding` | studio_id, logo_key, colors (jsonb), fonts (jsonb) |
| `studio_domains` | studio_id, hostname (único), kind, verified_at |
| `studio_payment_accounts` | studio_id, provider, provider_account_ref, status |
| `sessions` | id, user_id, token_hash, created_at, expires_at, revoked_at, user_agent |

### B1 — Entrega
| Tabela | Campos principais |
|---|---|
| `clients` | id, studio_id, name, email, phone, notes (sem senha) |
| `client_access` | id, studio_id, client_id, gallery_id, token_hash (único), pin_hash (opcional), expires_at, used_at, revoked_at, access_count |
| `packages` | id, studio_id, kind (`A`/`B`/`C`/`D`), name, price_cents, edited_quota, extra_edit_price_cents, deposit_percent, preview_ttl_days, edit_deadline_days, delivery_link_ttl_days, active |
| `events` | id, studio_id, client_id, package_id, title, event_date, terms (jsonb, cópia dos valores do pacote), total_cents, financial_status (`pending`/`partial`/`paid`), delivered_at, canceled_at, originals_expire_at, delivery_expire_at |
| `galleries` | id, studio_id, event_id, title, status (`draft`/`published`/`selection_closed`/`in_editing`/`ready`/`delivered`/`expired`), published_at, preview_expires_at, selection_closed_at, reopen_count, created_by |
| `photos` | id, studio_id, gallery_id, original_key, sha256 (índice `(studio_id, gallery_id, sha256)`, sem unicidade), width, height, size_bytes, **taken_at** (EXIF, lido antes de remover), sort_index, status (`uploaded`/`processing`/`ready`/`failed`), original_deleted_at |
| `photo_derivatives` | id, studio_id, photo_id, kind (`thumb`/`preview`), storage_key, width, height, size_bytes, expires_at, deleted_at |
| `favorites` | studio_id, client_id, photo_id, created_at |
| `photo_selections` | studio_id, gallery_id, photo_id, client_id, status (`selected`/`in_editing`/`edited`), is_extra, order_id, confirmed_at |
| `photo_comments` | id, studio_id, photo_id, client_id, body, created_at |
| `edited_files` | id, studio_id, photo_id, storage_key, sha256, size_bytes, uploaded_by, uploaded_at, deleted_at |
| `delivery_packages` | id, studio_id, event_id, kind (`edited`/`originals`), status (`building`/`ready`/`failed`/`expired`), zip_key, size_bytes, built_at, expires_at |
| `orders` | id, studio_id, event_id, client_id, kind (`deposit`/`balance`/`full`/`extra_edits`/`album`/`reopen`), status (`pending`/`paid`/`canceled`/`refunded`), total_cents |
| `payments` | id, studio_id, order_id, provider, provider_ref (único), status, amount_cents, paid_at |
| `refunds` | id, studio_id, payment_id, amount_cents, reason (`studio_refund`/`med`/`chargeback`), provider_ref (único), status (`pending`/`done`/`failed`), requested_by, created_at, done_at |
| `webhook_events` (global) | id, provider, event_id (único por provider), payload_hash, received_at, processed_at |
| `downloads` | id, studio_id, client_id, event_id, photo_id (nulo no ZIP), kind (`original`/`edited`/`zip`), at, ip_hash |

### B2 — Álbuns
| Tabela | Campos principais |
|---|---|
| `album_sizes` | id, studio_id, name, width_mm, height_mm, min_pages, max_pages, price_cents, active |
| `albums` | id, studio_id, event_id, size_id, status (§5), sequence_version, submitted_at, approved_at |
| `album_items` | id, studio_id, album_id, photo_id, position, note |
| `album_proofs` | id, studio_id, album_id, version, status (`sent`/`changes_requested`/`approved`), sent_at, decided_at |
| `album_proof_pages` | id, studio_id, proof_id, position, storage_key, client_comment |
| `album_guests` | id, studio_id, album_id, token_hash, expires_at |

### LGPD e auditoria
| Tabela | Campos principais |
|---|---|
| `consents` | id, studio_id, client_id, purpose (`delivery`/`portfolio`/`marketing`), is_minor_data, guardian_name, text_version, granted_at, revoked_at |
| `data_requests` | id, studio_id, client_id, type (`access`/`correction`/`deletion`), status, opened_at, closed_at |
| `audit_log` | id, studio_id (nulo para eventos da plataforma), actor_id, action, entity, entity_id, at, ip_hash, meta (jsonb); **somente inserção** |

B3 (site, agenda, contratos, financeiro, fila de edição): detalhar depois do beta. Índices em chaves estrangeiras e em `(studio_id, ...)`. Unicidade e checagens no banco, não só na aplicação.
`studio_usage` é cache: uma rotina periódica recalcula a partir da soma de `size_bytes` dos arquivos não apagados, que é a fonte da verdade.

---

## 11. Fotos: proteção, entrega e ciclo de vida

**Tipos de arquivo** (cada um com seu ciclo de vida): originais, prévias, pacote de entrega.

**Upload**
1. O fotógrafo pede à API uma URL assinada de envio. A API valida papel, estúdio, **cota do plano**, tipo e tamanho.
2. O arquivo vai direto ao bucket privado, em `studios/{studio_id}/...`, com chave aleatória.
3. A API finaliza e enfileira o processamento; `studio_usage` é atualizado.

**Processamento (worker)**
- Verificar o tipo pelo conteúdo real; aceitar só JPEG e PNG, em originais **e em editadas**. RAW, HEIC e vídeo ficam fora do B1.
- Foto repetida na mesma galeria (mesmo `sha256`): avisar o fotógrafo no upload, sem bloquear.
- Limite de pixels e de tamanho (proteção contra "bomba de descompressão").
- Ler `taken_at` do EXIF, corrigir orientação e **remover o EXIF** dos derivados (pode ter GPS).
- Gerar `thumb` (~400 px) e `preview` (lado maior ≤ ~1200 px, WebP de qualidade moderada) com **marca d'água diagonal repetida** (código da galeria; opcionalmente o nome do estúdio). Nomes de objeto aleatórios.

**Entrega**
- O **original nunca chega ao navegador antes de a matriz de liberação permitir** (§4.3).
- Prévias e miniaturas por URL assinada curta, só após checar: cliente com acesso à galeria, galeria publicada e não expirada, mesmo estúdio.
- Downloads (originais, editadas, ZIP) por URL assinada curta, emitida só depois de `services/release.py` autorizar, com registro em `downloads`.
- **ZIP**: montado em segundo plano em modo contínuo (sem carregar tudo na memória), com limite de tamanho; o link assinado é renovável pelo fotógrafo.
- Não usar o otimizador de imagens do Next para fotos de clientes.

**Expiração e retenção**: tabela em §4.6. Aviso por e-mail 1 dia antes das prévias vencerem. Prorrogação registrada no `audit_log`. Rotina agendada apaga o que venceu e atualiza `studio_usage`.

**Limitação assumida:** não dá para impedir 100% das capturas de tela. A defesa real é prévia pequena, marca d'água, original inacessível e limites de acesso. Bloquear o botão direito é cosmético. Alertar sobre acessos em massa: contador por `client_access` e limite de downloads por link e por hora (S-04), com aviso ao fotógrafo (tarefa 017).

---

## 12. Planos, cotas e custos de armazenamento

- Entitlements por plano (proposta; valores em D-12): `storage_gb`, `max_members`, `albums_per_month`, recursos habilitados. Cotas **verificadas no servidor** no upload e medidas em `studio_usage`.
- Até a 020, todo estúdio usa um **plano padrão semeado** pela migração (valores fictícios), para que a 010 já imponha cotas.
- Custo (preços públicos consultados em 02/11/2026; **confirmar nos sites oficiais**): Cloudflare R2 cerca de US$ 0,015/GB-mês, sem cobrança de saída; Backblaze B2 cerca de US$ 6,95/TB-mês, com saída grátis até 3× o armazenado. Para 100 GB, 500 GB e 1 TB: R2 aprox. US$ 1,50, 7,50 e 15; B2 aprox. US$ 0,70, 3,50 e 7.
- Isso é só armazenamento. Somar taxas de Pix/cartão, impostos, e-mail, WhatsApp, hospedagem, suporte e IA; converter pela cotação do dia.
- **Trial** (referência: 30 dias sem cartão): cota reduzida, verificação de e-mail, limites de upload e **limpeza automática** após o fim sem conversão, com aviso (D-14).

---

## 13. Segurança

| ID | Requisito | Tarefa |
|---|---|---|
| S-01 | Sessão opaca no servidor; cookie `HttpOnly`, `Secure`, `SameSite=Lax`; expiração curta e revogação | 006 |
| S-02 | argon2id; bloqueio progressivo após falhas | 006 |
| S-03 | 2FA TOTP obrigatório para donos de estúdio e admins | 008 |
| S-04 | Rate limiting em login, link de acesso, download e formulários (por IP e por estúdio) | 006, 017 |
| S-05 | RBAC (platform_admin, studio_owner, studio_member, assembler, client) | 007a |
| S-06 | Autorização **por recurso e por estúdio** em toda rota; testes de IDOR | 007a |
| S-07 | IDs públicos aleatórios (UUID) | 005 |
| S-08 | CSRF em ações que alteram dados | 006 |
| S-09 | CORS por `.env`, explícito | 003 |
| S-10 | Cabeçalhos de segurança no backend | 003 |
| S-11 | CSP, HSTS, `nosniff`, `frame-ancestors 'none'`, Referrer-Policy, Permissions-Policy no frontend | 004 |
| S-12 | Validação de toda entrada (Pydantic) e limite de corpo | 003 |
| S-13 | Somente consultas parametrizadas (ORM) | 005 |
| S-14 | Validação de upload por conteúdo, tipo, tamanho e limite de pixels | 010–011 |
| S-15 | Bucket privado, URLs assinadas curtas | 010 |
| S-16 | Webhooks (pagamento e assinatura) com assinatura verificada e idempotência | 016a, 020 |
| S-17 | Segredos só em variáveis de ambiente; varredura de segredos (gitleaks) | 004 |
| S-18 | Lockfiles versionados; `pip-audit` e `npm audit` no CI; Dependabot | 004 |
| S-19 | Next.js sempre na versão corrigida mais recente (houve falhas críticas em 2026; conferir o aviso vigente a cada atualização) | contínuo |
| S-20 | Erros sem stack trace; timeouts em chamadas externas | 003 |
| S-21 | Logs estruturados sem PII/segredos, com `request_id` e `studio_id` | 007b |
| S-22 | `audit_log` somente inserção | 005, 007b |
| S-23 | Backups automáticos e **teste de restauração** | 021 |
| S-24 | TLS, HSTS, Cloudflare/WAF, firewall, SSH por chave | 021 |
| S-25 | Contêiner sem root; menor privilégio nos tokens de storage | 021 |
| S-26 | Revisão de segurança em **contexto limpo** (subagente), separada de quem escreveu o código; auditoria final com ferramentas automáticas e avaliação de revisão humana nos pontos de pagamento e isolamento (D-11) | 040 |
| S-27 | Isolamento por estúdio: `studio_id` em tudo + RLS; papel do banco sem `BYPASSRLS` | 005B, 007a |
| S-28 | Testes automáticos de isolamento entre estúdios em todas as rotas | 007a |
| S-29 | Storage com prefixo por estúdio; URL assinada só após checar estúdio | 010 |
| S-30 | Sites dos estúdios em domínio separado do app; CSP restritiva | 029 |
| S-31 | Sanitização de todo conteúdo escrito pelo estúdio (sem HTML cru) | 029 |
| S-32 | Slugs reservados; proteção contra tomada de subdomínio; domínio próprio verificado | 029, 038 |
| S-33 | Cotas e limites por estúdio (armazenamento, uploads, requisições) | 010, 020 |
| S-34 | Acesso de suporte da plataforma restrito, justificado e auditado | 007b, 021 |
| S-35 | Matriz de liberação decidida no servidor em todo download; teste por estado financeiro e de edição | 017 |
| S-36 | Pagamento confirmado só por webhook; estado financeiro calculado dos pagamentos confirmados; conciliação | 016a |
| S-37 | ZIP e links de entrega: assinados, curtos, vinculados ao evento e ao cliente, renováveis só pelo fotógrafo | 019 |
| S-38 | Toda liberação e todo download registrados (`downloads`, `audit_log`) | 017, 019 |
| S-39 | Diagramador convidado: acesso restrito a um álbum, com validade e registro de acessos | 027 |
| S-40 | Resolução pré-contexto (§8 regra 8): funções `SECURITY DEFINER` mínimas, `search_path` fixo, sem `BYPASSRLS`; testes de token inválido, expirado, revogado e de outro estúdio | 005B, 009, 016a |
| S-41 | Estorno, MED ou cancelamento recalcula o estado financeiro e revoga links de entrega; teste da matriz após estorno | 016a, 017 |

---

## 14. LGPD

> Guia técnico, não aconselhamento jurídico. **Um advogado deve revisar** termos de uso, política de privacidade, contrato de operador, autorização de imagem e política de conteúdo antes do beta com dados reais.

**Papéis:** fotógrafo/estúdio = **controlador** dos dados dos clientes dele (inclusive fotos e fotos de crianças); plataforma = **operadora**; plataforma = **controladora** dos dados dos próprios fotógrafos.

| ID | Requisito |
|---|---|
| L-01 | Termos de uso e **contrato de operador** com cada estúdio no cadastro; lista de suboperadores (hospedagem, storage, e-mail, pagamento) |
| L-02 | Ferramentas para o estúdio cumprir a LGPD: registro de consentimentos, modelos de texto, exclusão e retenção configuráveis |
| L-03 | Fotos de **crianças e adolescentes**: consentimento específico e em destaque de ao menos um dos pais/responsável (art. 14), em `consents`. Redação com revisão jurídica (D-21) |
| L-04 | Autorização de uso de imagem para portfólio/redes **separada** da contratação |
| L-05 | Não usar **reconhecimento facial** (dado biométrico) |
| L-06 | Política de privacidade da plataforma, encarregado e canal de direitos do titular (`data_requests`) |
| L-07 | Retenção e eliminação automatizadas (§4.6); exclusão sob pedido. Prazos claros para o cliente |
| L-08 | Minimização: dados de pagamento ficam com o provedor |
| L-09 | Registro das operações em `docs/lgpd/` e relatório de impacto quando aplicável |
| L-10 | **Incidente**: runbook pronto; prazo de 3 dias úteis para comunicar a ANPD e os titulares (em dobro para agentes de pequeno porte; verificar enquadramento); registro por 5 anos; prazo contratual para a operadora avisar o controlador |
| L-11 | Avaliar transferência internacional (storage, e-mail, IA fora do Brasil) |
| L-12 | **Conteúdo e abuso**: termos, canal de denúncia e processo de remoção |
| L-13 | Acesso da equipe da plataforma aos dados dos estúdios: mínimo necessário e auditado (S-34) |
| L-14 | Cookies/analytics: consentimento só para itens não essenciais |

**Pagamentos:** usar provedor com **subcontas e divisão de pagamento**. Separar a cobrança de assinaturas (plataforma → estúdio) das vendas (cliente → estúdio). Consultar contador sobre impostos e notas.

---

## 15. Qualidade, agentes, modelos, skills e MCPs

- **Definição de pronto (DoD):** critérios de aceite atendidos; `ruff`, `mypy`, `pytest` verdes; `tsc`, ESLint e build do frontend verdes quando tocado; itens S-xx e L-xx da tarefa cumpridos e testados; **teste de isolamento entre estúdios** quando a tarefa criar ou alterar rotas; **teste por estado da matriz** (§4.3) quando mexer em download; sem dependências novas sem aprovação; documentação atualizada; relatório em `docs/reviews/NNN-nome.md`; `docs/RETOMADA.md` atualizado; commit feito.
- **Testes por rota protegida:** sem login (401), papel errado (403), recurso de outro usuário ou **outro estúdio** (403/404), caso feliz.
- **CI:** lint, tipos, testes, `pip-audit`, `npm audit`, gitleaks, build.
- **Ferramenta única: Claude Code.** O OpenCode foi descontinuado (revisão Opus 001; remoção dos arquivos em D-31). `AGENTS.md`, `opencode.json` e `.opencode/` não são fonte de regra.
- **Agentes (Claude Code):** a **sessão principal** planeja e implementa. Subagentes em `.claude/agents/`: `Explore` (Haiku; Read, Grep, Glob), `postgres-dba` (Read, Grep, Glob), `change-reviewer` e `security-reviewer` (Bash só para leitura: `git diff/log/show` e checks). Todos somente leitura, em contexto limpo.
- **Modelos e tokens:** Sonnet é o padrão. Haiku para exploração e tarefas mecânicas. **Opus só em último caso, com aprovação do Fagner, para planejar algo complexo.** Regras e quando dar `/clear` na skill `economia-de-tokens`.
- Dados reais nunca entram em prompts (regra 4 do §0.1).

### Skills e MCPs (só os que a tarefa listar)

| Quando | Skills/MCPs |
|---|---|
| 003–004 | Nenhum |
| 005–009 | Nenhuma instalada. Skills de LGPD (ex.: `lgpd-data-mapping`, `lgpd-consent-schema`, `lgpd-dsar`) só depois de conferir a origem e com aprovação |
| 021, 039 | Skills de LGPD aprovadas até lá, com revisão jurídica |
| 013, 024–025, 028–029, 038 | `frontend-design`, web-interface-guidelines, GSAP (se aprovada), `chrome-devtools-mcp` (perfil isolado, sem telemetria), 21st MCP (somente busca) |
| 040 | `security-audit` (Cloudflare), se aprovada e instalada em `.claude/skills/` |
| Nunca por padrão | `superpowers` (fluxos obrigatórios conflitam com este processo); só skills avulsas aprovadas: `test-driven-development`, `systematic-debugging`, `verification-before-completion` |

---

## 16. Roadmap (Etapas)

### Etapa 0 — Fundação
- **003** Backend: reorganização + hardening base (sem Postgres): `app/`, `core/config.py`, CORS por `.env`, cabeçalhos, limite de corpo e erros, `pyproject.toml` + ruff/mypy/pytest, venv, pin do FastAPI atualizado para a versão validada, testes de `/health`, `.gitignore` ampliado.
- **004** Frontend e raiz: limpar boilerplate, estrutura `src/`, lockfile, cabeçalhos no `next.config`, `.editorconfig`, `infra/docker-compose.yml`, CI, Dependabot, gitleaks, ADR-001 a 009.
- **005** PostgreSQL + SQLAlchemy 2 + Alembic: `users`, `sessions`, `audit_log` (somente inserção), testes de integração em contêiner. **Concluída, sem RLS** (o multi-tenant passou para a 005B).
- **005B** Multi-tenant: ADR-007 aprovada antes; `studios`, `studio_members`, `audit_log.studio_id`, papéis de runtime e de migração (runtime sem `BYPASSRLS`), RLS fail-closed, `SET LOCAL` seguro, classificação das tabelas (§10), funções de resolução pré-contexto (§8 regra 8, S-40) e testes A/B. Spec em `docs/tasks/005B-*.md` (rascunho, aguarda aprovação).

### Etapa 1 — Identidade e acesso
- **006** Login (dono e admin), sessão, logout, argon2id, bloqueio, rate limit, CSRF.
- **007a** RBAC, autorização por recurso e estúdio, **testes de isolamento** (base reutilizável para todas as rotas).
- **007b** `audit_log` nas ações, logging estruturado (S-21) e acesso de suporte auditado (S-34).
- **008** 2FA TOTP.
- **009** Acesso do cliente final (link mágico e/ou PIN, D-05) pela função de resolução (S-40), link copiável para cliente sem e-mail (D-28) e consentimento inicial. E-mail via Mailpit no dev; o provedor real (D-03) é decidido antes da 021.

### Etapa 2 — B1: base de galerias e fotos
- **010** Storage S3 (MinIO no dev), upload assinado, validações, `studio_usage` e cotas pelo plano padrão semeado (§12).
- **011** Worker de imagens: derivados WebP, marca d'água, `taken_at`, limites, aviso de duplicata (D-26 antes).
- **012a** Clientes, **pacotes A/B/C** e eventos: modelos, CRUD, cópia de `terms`, cancelamento.
- **012b** Galerias: CRUD, máquina de estados (§4.2) validada no servidor, publicar, prazos configuráveis.
- **013** Galeria do cliente (API e tela): marca do estúdio, mobile first, filtros, slideshow e animações (§4.9).
- **014** Favoritos, comentários e **seleção por regra do pacote** (A nenhuma, B cota, C quantidade fixa), cálculo de extras, confirmação da seleção.
- **015** Encerramento da seleção, expiração das prévias e notificações por e-mail ao cliente e ao fotógrafo (§4.5.1).

### Etapa 3 — B1: pagamento, edição e entrega
- **016a** Pedidos e pagamentos com **provedor fictício** (adapter): `orders`, `payments`, `refunds`, `webhook_events`; webhook assinado e idempotente; resolução por `provider_ref` (S-40); estado financeiro calculado; estorno (S-41); conciliação. Não depende de D-01.
- **016b** Provedor real em sandbox (D-01), subconta/split, sinal, saldo e adicionais.
- **017** **Matriz de liberação** (`services/release.py`, ADR-009 antes), download de originais (A e B) por URL assinada curta, registro de downloads, teste da matriz após estorno e limite de acessos por link (§11).
- **018** Edição mínima: status por foto, prazo de edição, área de entrega para o editor (ou dono) subir as editadas.
- **019** Pacote de entrega: ZIP em segundo plano, link assinado renovável, e-mail e expiração conforme retenção (§4.6).
- **020** Planos, cotas, assinatura e trial (cobrança da plataforma ao estúdio).
- **021** **Pré-beta:** LGPD mínima (termos, privacidade, contrato de operador, direitos do titular, denúncia/remoção), canal de suporte ao estúdio (e-mail), provedor de e-mail real (D-03), revisão de segurança do que existe, backups com teste de restauração, staging.
- **022** **Beta fechado** com fotógrafos reais (meta 3 a 5; em 03/11/2026 há 1 ou 2 confirmados, que aceitam o B1 sem álbuns), B1 completo. Decisão de rumo: o que entra no B3. A ordem B2 → B3 só muda por decisão do Fagner.

### Etapa 4 — B2: álbuns (Pacote D)
- **023** Modelo de álbum, tamanhos e regras de páginas; criar o álbum a partir da galeria; cliente escolhe as fotos.
- **024** **Sequência**: ordenar por arrastar e soltar (e toque no celular), sugestão por `taken_at`, comentário por foto, salvamento com versão, confirmação que trava a sequência.
- **025** Ilustração: visualização folheável do álbum no formato escolhido.
- **026** Prova e aprovação: estúdio sobe as lâminas diagramadas fora do sistema, cliente comenta, pede ajuste ou aprova, histórico de versões.
- **027** Exportação para produção (ZIP numerado + manifesto), diagramador convidado e limites por plano.

### Etapa 5 — B3: gestão do estúdio e site (ordem definida pelo beta)
- **028** Identidade visual e design system.
- **029** Site do estúdio: gerado automaticamente, construtor de páginas, tema, subdomínio, domínio separado do app.
- **030** CRM, clientes e Kanban.
- **031** Agenda e agendamento online.
- **032** Contratos e assinatura eletrônica (D-17).
- **033** Briefing e questionários.
- **034** E-mails e WhatsApp automatizados (D-16).
- **035** Financeiro e dashboard (receitas, pendentes, previsão de Pix, faturamento por evento).
- **036** Fila de edição, atribuição a editores e SLA.
- **037** Métricas de vendas de fotos extras e de armazenamento por cliente e plano.
- **038** Domínio próprio e SEO.

### Etapa 6 — Lançamento
- **039** LGPD operacional completa (retenção por estúdio, exportar/excluir, relatórios).
- **040** Revisão de segurança final, testes de abuso e de isolamento, auditoria de dependências, checklist OWASP ASVS.
- **041** Monitoramento, runbook de incidente, deploy de produção (VPS + Cloudflare), checklist de go-live.

---

## 17. Decisões pendentes (REQUEREM APROVAÇÃO do Fagner)

| ID | Decisão |
|---|---|
| D-01 | Provedor de Pix com subcontas/split (Mercado Pago, Asaas, Stripe etc.) e **quem recebe o Pix**: o fotógrafo direto ou a plataforma |
| D-02 | Storage: Cloudflare R2 ou Backblaze B2 |
| D-03 | E-mail transacional |
| D-04 | Hospedagem, domínio da plataforma e domínio separado para sites dos estúdios |
| D-05 | Acesso do cliente final: link mágico, PIN ou ambos |
| D-06 | Tamanhos de álbum, regras de páginas e limite de fotos por álbum |
| D-07 | Retenção dos originais (sugerido 60 dias após a entrega) e do pacote de entrega (sugerido 30 dias), por plano |
| D-08 | Encarregado (nome e contato) e modelos de contrato/autorização de imagem |
| D-09 | shadcn/ui? Identidade visual da plataforma |
| D-10 | Diagramador: papel interno, convidado externo ou ambos |
| D-11 | Revisão jurídica (e revisão humana de segurança): quem e quando, antes do beta com dados reais |
| D-12 | Planos, preços e cotas |
| D-13 | Monetização: assinatura, comissão sobre vendas ou mista |
| D-14 | Trial: duração, cota, anti-abuso e limpeza |
| D-15 | Nome e marca (consultar advogado/INPI) |
| D-16 | WhatsApp: provedor e custos, ou só e-mail no início |
| D-17 | Contratos: assinatura eletrônica própria ou provedor; validade jurídica |
| D-18 | Prazo para quitar o saldo e o que acontece com os arquivos se não for pago |
| D-19 | Cobrança da reabertura de galeria e quantas reaberturas são permitidas |
| D-20 | Valor da edição extra no pacote A |
| D-21 | Tratamento de fotos de crianças e adolescentes (texto e fluxo de consentimento) |
| D-22 | Confirmar valores sugeridos: sinal de 50%, prévias de 3 dias, link de entrega de 30 dias; e se o cliente pode confirmar a seleção com o evento PENDENTE (§4.3) |
| D-23 | Escopo do álbum: diagramação 100% externa, sem editor de lâminas no sistema; vídeo de diagramação fora |
| D-24 | Significado de "ilustração" do álbum (§5, item 4) |
| D-25 | Cobrança do Pacote D: valor, sinal e extras de página |
| D-26 | Tecnologia da fila e do agendador de rotinas (imagens, ZIP, expiração); decidir antes da 011 |
| D-27 | Reembolso, estorno e MED do Pix: quem inicia (sugerido: só o fotógrafo), reembolso parcial, efeito na liberação (sugerido: recálculo e revogação, §4.3) |
| D-28 | Cliente sem e-mail (sugerido: link copiável enviado pelo fotógrafo, sem integração de WhatsApp no B1) |
| D-29 | Prazo de edição vencido (sugerido: aviso ao dono por e-mail, sem ação automática no B1) |
| D-30 | Cobrança do Claude Code: API ou assinatura, com teto de US$ 50/mês (sugerido: medir 1 semana com `/usage` e decidir) |
| D-31 | Aposentar o OpenCode: remover `.opencode/`, `opencode.json*`, `prompts/`, `AGENTS.md`, `CLAUDE.old.md` e encerrar 003D/003F/003H como descontinuadas (sugerido: sim, após o vencimento do ciclo pago) |
| D-32 | Resolução pré-contexto sob RLS (§8 regra 8): funções `SECURITY DEFINER` mínimas ou tabela global de roteamento (sugerido: funções) |

---

## 18. Riscos

| Risco | Mitigação |
|---|---|
| Um estúdio acessar dados de outro | `studio_id` + RLS + testes de isolamento em todas as rotas |
| Original liberado antes do saldo | Matriz decidida só no servidor (`services/release.py`), teste por estado, registro de downloads |
| Pagamento marcado como pago sem estar | Só webhook assinado e idempotente; estado calculado; conciliação |
| Estorno ou MED depois do download liberado | `refunds` por webhook, recálculo, revogação de links (S-41); registro em `downloads` para disputa |
| Lookup pré-contexto virar brecha no RLS | Funções mínimas e testadas, sem `BYPASSRLS` (S-40); revisão do `postgres-dba` e do `security-reviewer` |
| Custo de IA acima do teto | Sonnet padrão, Haiku no `Explore`, esforço `medium`, `/clear` entre tarefas, medir com `/usage` (D-30) |
| Escopo gigante (concorrente maduro) | Três blocos; B1 como MVP; beta antes dos demais |
| Custo de armazenamento fora de controle | Cotas por plano, trial limitado, expiração, métricas por estúdio |
| ZIP grande derrubar o servidor | Montagem em segundo plano, em modo contínuo, com limite de tamanho |
| Dados reais em prompts de IA | Dados fictícios; `.env` bloqueado em `.claude/settings.json` |
| Falhas críticas no Next.js | Atualização contínua, Dependabot, contenção (sem root, tokens mínimos) |
| Pacotes inventados pela IA | Conferir nome/origem; instalação só com aprovação |
| XSS em conteúdo do estúdio | Sanitização, CSP restritiva, domínio separado |
| Vazamento de fotos | Bucket privado, URLs curtas, auditoria, rate limit |
| Questões legais (LGPD, pagamentos, abuso, marca) | Revisão jurídica e contábil antes do beta |
| Perda de dados | Backups e teste de restauração |

---

## 19. Glossário

- **Estúdio (tenant):** o espaço de um fotógrafo na plataforma. **Cliente final:** cliente do fotógrafo.
- **Evento:** o trabalho contratado (pacote, preço, estado financeiro). A galeria pertence a um evento.
- **Pacote (A/B/C/D):** modalidade de entrega contratada.
- **Sinal:** primeira parte do pagamento (ex.: 50%); o saldo é o restante.
- **Prévia:** versão pequena e com marca d'água, válida pelo prazo da galeria. **Original:** arquivo em alta qualidade.
- **Pacote de entrega:** arquivos editados mais o ZIP, liberados por link assinado.
- **Sequência:** a ordem das fotos no álbum. **Lâmina:** par de páginas. **Prova:** imagens das lâminas enviadas ao cliente para aprovação.
- **RLS:** segurança por linha no PostgreSQL. **IDOR:** acessar o recurso de outra pessoa trocando um ID na URL.

---

## 20. Status

O detalhe de cada tarefa vive em `docs/RETOMADA.md`. Atualize esta tabela só quando uma etapa inteira terminar.

| Etapa | Escopo | Status |
|---|---|---|
| 0 | 003–005B Fundação | em andamento: 003–005 concluídas; 005B aguarda aprovação (ADR-007, D-32) |
| 1 | 006–009 (com 007a/007b) Identidade e acesso | pendente |
| 2 | 010–015 (com 012a/012b) B1 base | pendente |
| 3 | 016a–022 B1 pagamento, edição, entrega, pré-beta e beta | pendente |
| 4 | 023–027 B2 Álbuns | pendente |
| 5 | 028–038 B3 Gestão e site | pendente |
| 6 | 039–041 Lançamento | pendente |
