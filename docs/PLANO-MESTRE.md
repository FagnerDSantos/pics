# PLANO MESTRE v2 — Pics (plataforma para fotógrafos)

> Documento de referência para pessoas e agentes de IA. Leia inteiro antes de qualquer tarefa.
> Dono do produto e decisor final: **Fagner**. Versão 2 — 02/11/2026. Substitui a versão 1.
> Fonte da verdade de escopo, arquitetura e regras. Ao concluir uma tarefa, atualize a seção 20 (Status).
> **Mudança principal da v1 para a v2:** o produto não é o sistema de um único estúdio. É uma **plataforma (SaaS) oferecida a vários fotógrafos**, cada um com seu site, seus clientes, suas galerias e seu financeiro, em três blocos de entrega.

---

## 0. Como usar este documento (regras para agentes)

1. Leia este plano e o `CLAUDE.md` antes de agir.
2. Trabalhe **uma tarefa por vez**, a partir de `docs/tasks/NNN-nome.md` (modelo em `docs/tasks/_modelo.md`).
3. Não saia do escopo da tarefa. O que estiver fora do escopo vai para `docs/reviews/` como observação, sem correção por conta própria.
4. Tudo marcado **REQUER APROVAÇÃO** (seção 17 e regras do `CLAUDE.md`) só avança com aprovação explícita do Fagner.
5. Use **dados fictícios**. Nunca coloque fotos reais, dados de clientes, chaves ou `.env` em prompts, logs, testes ou commits. Modelos gratuitos podem coletar o que recebem.
6. `git commit` antes e depois de cada tarefa. No máximo 2 rodadas de correção; depois pare e consulte.
7. Antes de instalar qualquer pacote, confirme que o nome existe e é o oficial. Novas dependências **REQUEREM APROVAÇÃO**.
8. Nunca use o modo de aprovação automática (`--auto`).
9. **Toda tabela de negócio tem `studio_id`** e toda consulta respeita o estúdio (seção 6). Isso nunca é opcional.
10. Skills e MCPs: só os que a tarefa listar (seção 15).

---

## 1. Visão do produto

Uma plataforma web para fotógrafos e estúdios venderem, entregarem e gerenciarem seu trabalho. Cada fotógrafo (um **estúdio**) tem seu espaço, sua marca, seus clientes e suas galerias.

### Os três blocos (ordem de entrega definida pelo Fagner)

| Bloco | Conteúdo | Meta |
|---|---|---|
| **B1 — Entrega de fotos** | Galerias de prova e de entrega, favoritos, seleção, pagamento, download dos originais, e-mails automáticos, planos e cotas | **MVP**: ser usado por 3 a 5 fotógrafos reais |
| **B2 — Site e gestão do estúdio** | Site personalizado por fotógrafo, CRM, agenda e agendamento online, contratos, briefing, e-mails/WhatsApp, financeiro, marketing | Construído a partir do que o beta pedir |
| **B3 — Álbuns** | Seleção ordenada, tamanho, ilustração do layout, prova ao cliente e exportação para quem monta o álbum | Possível diferencial; pode subir de prioridade conforme o beta |

### Restrições do projeto

- **Custo baixo**: infraestrutura barata e sem custo de saída de dados; IA gratuita só com dados fictícios.
- **Segurança forte**, com **isolamento entre estúdios** como risco nº 1 (seção 13).
- **LGPD desde o projeto**; o fotógrafo é o controlador dos dados dos clientes dele e a plataforma é a operadora (seção 14).
- **Visual extraordinário** no site e nas áreas logadas (B2).
- Desenvolvimento assistido por IA: tarefas pequenas, revisáveis e com critérios de aceite claros.

---

## 2. Referência competitiva: Davions (consultado em 02/11/2026)

> Referência de **funcionalidades e preços**. Não copiar textos, layout, identidade visual nem código. Confirmar os dados no site deles antes de decidir preços.

### Funcionalidades (todos os planos, salvo indicação)

Kanban; CRM; cadastro de clientes; agendamento online; contratos automáticos; questionários personalizados; e-mails e WhatsApp automatizados; galeria de provas e de entrega final; integração com Lightroom; site profissional com SEO e IA; financeiro.
**"Em breve" no site deles:** diagramador de álbuns (limites mensais por plano), blog com IA, posts de redes sociais com IA, loja integrada, e-mail marketing.

### Planos e preços

| Plano | Preço/mês | Armazenamento | Diferenças |
|---|---|---|---|
| Standard | R$ 149 (de R$ 199) | 100 GB | Sem equipe e sem multi agenda |
| Pro | R$ 299 (de R$ 399) | 500 GB | Até 5 membros de equipe |
| Ultimate | R$ 449 (de R$ 599) | 1.000 GB | Multi agenda, equipe ilimitada |

Teste grátis de 30 dias, sem cartão. Agendamentos ilimitados em todos. Diagramador de álbuns previsto como 3, 12 e ilimitado por mês.

### O que isso ensina

- **Armazenamento é o eixo dos planos** e o maior custo variável (seção 11).
- A equipe com permissões (membros) é recurso de plano: o modelo de papéis precisa suportar isso.
- O diagramador de álbuns já está no radar deles. O diferencial do B3 precisa ser definido (ver seção 12).
- Trial de 30 dias sem cartão atrai abuso: precisa de cota reduzida e limpeza (seção 11).

---

## 3. Atores e fluxo principal do B1

| Ator | Descrição |
|---|---|
| Admin da plataforma (`platform_admin`) | Fagner e equipe da plataforma. Gerencia estúdios, planos e suporte |
| Dono do estúdio (`studio_owner`) | O fotógrafo. Gerencia tudo do próprio estúdio |
| Membro do estúdio (`studio_member`) | Equipe, com permissões configuráveis |
| Diagramador (`assembler`) | Monta álbuns (interno ou convidado de fora, ver B3) |
| Cliente final (`client`) | Cliente do fotógrafo; vê galerias, seleciona, paga e baixa |
| Visitante | Navega no site do estúdio |

**Fluxo do B1:**

1. O fotógrafo cria o cliente e a galeria e faz upload em lote. O sistema gera as prévias.
2. Publica a galeria. O cliente recebe o acesso por e-mail. O prazo das prévias começa (padrão 3 dias, configurável).
3. O cliente vê as prévias, favorita e seleciona.
4. O cliente paga (Pix) conforme o pacote/valor definido pelo fotógrafo.
5. O sistema libera os originais por links assinados curtos e registra os downloads.
6. As prévias expiram e são apagadas. Os originais seguem a política de retenção do plano.

---

## 4. Requisitos funcionais

### B1 — Entrega de fotos
- RF-01 Cadastro e login do fotógrafo; criação do estúdio; convite de membros (conforme plano).
- RF-02 Cadastro de clientes do estúdio.
- RF-03 Criar galerias; upload em lote (JPEG/PNG) com progresso e retomada.
- RF-04 Publicar e despublicar; prazo das prévias configurável por galeria (padrão 3 dias) e prorrogável, com registro.
- RF-05 Galeria do cliente com a **marca do estúdio** (logo e cores), grade e tela cheia, mobile first.
- RF-06 Favoritar, selecionar e comentar fotos.
- RF-07 Pagamento do cliente final via Pix; acompanhamento de status.
- RF-08 Download dos originais após confirmação; registro de downloads.
- RF-09 E-mails automáticos (acesso, lembrete de prazo, pagamento, entrega).
- RF-10 Planos, cotas e cobrança do estúdio (assinatura, trial).
- RF-11 Painel do fotógrafo: uso de armazenamento, galerias, pedidos.
- RF-12 Direitos do titular (LGPD): pedido de acesso, correção e exclusão.

### B2 — Site e gestão do estúdio (épicos; detalhar após o beta)
- RF-13 Site do estúdio: páginas, tema, portfólio, contato, blog; subdomínio e depois domínio próprio; SEO.
- RF-14 CRM e Kanban de projetos.
- RF-15 Agenda e agendamento online.
- RF-16 Contratos gerados a partir do pacote e assinatura eletrônica.
- RF-17 Briefing e questionários personalizados.
- RF-18 E-mails e (avaliar) WhatsApp automatizados.
- RF-19 Financeiro: receitas, despesas, relatórios.
- RF-20 Marketing (posts, campanhas) — avaliar depois.

### B3 — Álbuns
- RF-21 Seleção do cliente ordenada (sugestão pelo horário da foto).
- RF-22 Montagem: reordenar por arrastar e soltar, lâminas, tamanho do álbum.
- RF-23 Ilustração do layout das lâminas.
- RF-24 Prova ao cliente e aprovação.
- RF-25 Exportação para produção (ZIP numerado + manifesto).
- RF-26 Diagramador convidado (acesso restrito a um álbum).

---

## 5. Requisitos não funcionais

- **Segurança**: seção 13. **LGPD**: seção 14.
- **Isolamento entre estúdios**: nenhum estúdio acessa dado, foto ou arquivo de outro.
- **Desempenho**: upload direto ao storage; processamento em worker; prévias leves; miniaturas; paginação.
- **Mobile first**: o cliente final escolhe fotos pelo celular.
- **Acessibilidade**: WCAG AA (contraste, teclado, `prefers-reduced-motion`).
- **Idioma**: pt-BR. Datas em UTC no banco.
- **Dinheiro**: sempre em centavos (inteiro).
- **Observabilidade**: logs estruturados com `request_id` e `studio_id`, sem dados pessoais nem segredos.
- **Custo**: medir armazenamento por estúdio e impor cotas.

---

## 6. Arquitetura (multi-tenant)

```
Navegador ──► Frontend (Next 16) ──► API (FastAPI) ──► PostgreSQL (RLS)
                                        │
                                        ├──► Storage S3-compatível PRIVADO (prefixo por estúdio)
                                        ├──► Worker de imagens (derivados + marca d'água)
                                        ├──► E-mail transacional
                                        └──► Provedor de Pix com subcontas/split (webhook assinado)
```

### Stack

| Camada | Escolha |
|---|---|
| Backend | Python 3.12 ou 3.13, FastAPI, Pydantic v2, pydantic-settings |
| Banco | PostgreSQL, SQLAlchemy 2, Alembic |
| Auth | Sessão opaca no servidor + cookie `HttpOnly`; argon2id; 2FA TOTP para dono/admin |
| Imagens | Pillow (ou pyvips), em worker |
| Storage | S3-compatível privado (Cloudflare R2 ou Backblaze B2; MinIO no dev) via boto3 e URLs assinadas |
| Frontend | Next 16, TypeScript estrito, Tailwind; shadcn/ui **REQUER APROVAÇÃO** |
| Qualidade | ruff, mypy, pytest, ESLint, `tsc`, CI no GitHub Actions |
| Infra local | Docker Compose: PostgreSQL, MinIO, Mailpit |

### Regras de multi-tenancy (obrigatórias)

1. **Estúdio = tenant.** Toda tabela de negócio tem `studio_id NOT NULL`, indexado.
2. **Chaves estrangeiras compostas** incluindo `studio_id` onde fizer sentido, para impedir referência entre estúdios.
3. **Row Level Security (RLS) no PostgreSQL** como segunda barreira: a aplicação define o estúdio da sessão (`SET LOCAL app.studio_id`), e o papel do banco usado pela API **não tem `BYPASSRLS`**. A checagem na aplicação continua obrigatória.
4. **Testes de isolamento**: para cada rota, criar dois estúdios e provar que A não lê, altera nem apaga dados de B (401/403/404).
5. **Storage**: chaves com prefixo `studios/{studio_id}/...`; URLs assinadas só após checar permissão e estúdio.
6. **Acesso da equipe da plataforma** a dados de estúdios só por "acesso de suporte" restrito, justificado e registrado no `audit_log`.
7. **Sites dos estúdios** (B2) servidos em **domínio separado** do app, para isolar cookies e limitar o impacto de XSS.

### Comunicação frontend e backend

Em produção, mesmo "site" para app e API (ex.: `app.dominio` e `api.dominio`), cookie `SameSite=Lax`, `Secure`, `HttpOnly`. Ações que alteram dados exigem proteção contra CSRF (token por sessão + verificação de `Origin`). CORS com origens e métodos explícitos, vindos do `.env`, nunca `*` com credenciais.

### ADRs a registrar em `docs/adr/` (status: proposta até aprovação)

001 Frontend e backend separados · 002 PostgreSQL + SQLAlchemy 2 + Alembic · 003 Sessão opaca com cookie `HttpOnly` · 004 Storage privado com URLs assinadas · 005 Imagens em worker com limites · 006 Dinheiro em centavos e webhooks idempotentes · 007 Multi-tenancy com `studio_id` + RLS · 008 Domínio separado para sites dos estúdios.

---

## 7. Estado atual (02/11/2026)

```
pics/
├─ backend/    main.py (tudo em 1 arquivo), requirements.txt, .env.example
├─ frontend/   Next 16 boilerplate
├─ docs/       tasks/, reviews/, _modelo.md, PLANO-MESTRE.md (v1)
├─ .opencode/  skills locais
├─ CLAUDE.md, README.md, opencode.json, .gitignore
```

**Problemas (resumo):** backend em um arquivo, sem testes/migrações/`pyproject.toml`; CORS e versão hardcoded; frontend ainda com boilerplate e sem lockfile versionado; sem `infra/`, CI, `.editorconfig`, `docs/adr/`; `.gitignore` incompleto; FastAPI global (0.141.1) diverge do pin (0.115.6): **atualizar o pin para a versão validada em teste, não rebaixar a global**; usar venv e Python 3.12 ou 3.13.
**Segurança que já existe:** CORS restrito a `localhost:3000`; `.env` fora do Git; `.env.example` com placeholders; agentes proibidos de ler `.env`; versões fixas no backend; TypeScript strict e ESLint; sem `dangerouslySetInnerHTML`.

---

## 8. Estrutura alvo

```
backend/
├─ app/
│  ├─ main.py
│  ├─ api/v1/{router.py, deps.py, routes/{health,auth,studios,clients,galleries,photos,orders,billing,webhooks,albums}.py}
│  ├─ core/{config.py, security.py, logging.py, tenancy.py}
│  ├─ db/{base.py, session.py}
│  ├─ models/  schemas/  repositories/
│  ├─ services/{storage.py, images.py, mail.py, payments.py, quotas.py, ...}
│  └─ workers/{process_photo.py, expire_galleries.py}
├─ alembic/
├─ tests/{conftest.py, unit/, integration/, isolation/}
└─ pyproject.toml  requirements.txt  requirements-dev.txt  .env.example
frontend/src/{app/, components/{ui,layout}, lib/, hooks/, types/, services/}
infra/docker-compose.yml        # PostgreSQL, MinIO, Mailpit
docs/{adr/, tasks/, reviews/, lgpd/}
.github/workflows/ci.yml  .github/dependabot.yml  .editorconfig
```

---

## 9. Modelo de dados (proposta — validar antes da migração)

PostgreSQL, chaves `uuid`, `timestamptz` (UTC), dinheiro em centavos. **Todas as tabelas de negócio têm `studio_id`.**

### Plataforma e estúdio

| Tabela | Campos principais |
|---|---|
| `studios` | id, name, slug (único, validado, com lista de nomes reservados), status, plan_id, created_at |
| `users` | id, email (citext único), password_hash, platform_role (`platform_admin`/nulo), full_name, is_active, totp_secret (criptografado) |
| `studio_members` | studio_id, user_id, role (`studio_owner`/`studio_member`/`assembler`), permissions (jsonb) |
| `plans` | id, name, price_cents, storage_gb, max_members, albums_per_month, features (jsonb), active |
| `subscriptions` | id, studio_id, plan_id, status (`trial`/`active`/`past_due`/`canceled`), trial_ends_at, current_period_end, provider_ref |
| `studio_usage` | studio_id, bytes_used, photos_count, updated_at |
| `studio_branding` | studio_id, logo_key, colors (jsonb), fonts (jsonb) |
| `studio_domains` | studio_id, hostname (único), kind (`subdomain`/`custom`), verified_at |
| `studio_payment_accounts` | studio_id, provider, provider_account_ref, status |
| `sessions` | id, user_id, token_hash, created_at, expires_at, revoked_at, user_agent |

### B1 — Entrega

| Tabela | Campos principais |
|---|---|
| `clients` | id, studio_id, name, email, phone, notes (clientes do estúdio; sem senha) |
| `client_access` | id, studio_id, client_id, gallery_id, token_hash, pin_hash (opcional), expires_at, used_at |
| `galleries` | id, studio_id, client_id, title, event_date, status (`draft`/`published`/`expired`/`closed`), published_at, preview_expires_at, preview_ttl_days, created_by |
| `photos` | id, studio_id, gallery_id, original_key, sha256, width, height, size_bytes, **taken_at** (EXIF, lido antes de remover), sort_index, status (`uploaded`/`processing`/`ready`/`failed`) |
| `photo_derivatives` | id, studio_id, photo_id, kind (`thumb`/`preview`), storage_key, width, height |
| `favorites` | studio_id, client_id, photo_id, created_at |
| `orders` | id, studio_id, gallery_id, client_id, status (`pending`/`paid`/`canceled`/`refunded`), total_cents |
| `payments` | id, studio_id, order_id, provider, provider_ref (único), status, amount_cents, paid_at |
| `webhook_events` | id, provider, event_id (único), payload_hash, received_at, processed_at |
| `downloads` | id, studio_id, client_id, gallery_id, photo_id, at, ip_hash |

### B3 — Álbuns

| Tabela | Campos principais |
|---|---|
| `album_sizes` | id, studio_id, name, width_mm, height_mm, min_pages, max_pages, price_cents, active |
| `albums` | id, studio_id, gallery_id, size_id, status (`draft`/`selecting`/`in_assembly`/`proof_sent`/`approved`/`delivered`), approved_at |
| `album_spreads` | id, studio_id, album_id, position, layout |
| `album_items` | id, studio_id, album_id, spread_id, photo_id, position, crop (jsonb) |

### LGPD e auditoria

| Tabela | Campos principais |
|---|---|
| `consents` | id, studio_id, client_id, purpose (`delivery`/`portfolio`/`marketing`), is_minor_data, guardian_name, text_version, granted_at, revoked_at |
| `data_requests` | id, studio_id, client_id, type (`access`/`correction`/`deletion`), status, opened_at, closed_at |
| `audit_log` | id, studio_id (nulo p/ eventos da plataforma), actor_id, action, entity, entity_id, at, ip_hash, meta (jsonb); **somente inserção** |

### B2 (a detalhar após o beta)
Páginas e tema do site, posts, agendamentos, contratos e assinaturas, questionários e respostas, lançamentos financeiros, campanhas.

Índices em chaves estrangeiras e em `(studio_id, ...)`. Unicidade e checagens no banco, não só na aplicação.

---

## 10. Fotos: proteção e ciclo de vida

**Upload**
1. O fotógrafo pede à API uma URL assinada de envio. A API valida papel, estúdio, **cota do plano**, tipo e tamanho.
2. O arquivo vai direto ao bucket privado, em `studios/{studio_id}/...`, com chave aleatória.
3. A API finaliza e enfileira o processamento. `studio_usage` é atualizado.

**Processamento (worker)**
- Verificar o tipo pelo conteúdo real; aceitar só JPEG e PNG.
- Abrir com limite de pixels (proteção contra "bomba de descompressão") e de tamanho.
- Ler `taken_at` do EXIF, corrigir a orientação e **remover o EXIF** dos derivados (pode ter GPS).
- Gerar `thumb` (~400 px) e `preview` (lado maior ≤ ~1200 px, JPEG de qualidade moderada) com **marca d'água diagonal repetida** (código da galeria; opcionalmente o nome do estúdio).
- Nomes de objeto aleatórios.

**Entrega**
- O **original nunca chega ao navegador antes do pagamento confirmado**.
- Prévias e miniaturas via URL assinada curta, emitida só após checar: cliente com acesso à galeria, galeria publicada e não expirada, mesmo estúdio.
- Após o pagamento, downloads por URL assinada curta, com registro em `downloads`.
- Não usar o otimizador de imagens do Next para fotos de clientes.

**Expiração**
- `preview_expires_at = published_at + preview_ttl_days` (padrão 3, configurável por galeria).
- Rotina agendada apaga prévias e miniaturas vencidas e marca a galeria como `expired`. Aviso por e-mail 1 dia antes. Prorrogação registrada no `audit_log`.
- Retenção dos **originais** depende do plano e da decisão D-07.

**Limitação assumida:** não é possível impedir 100% de capturas de tela. A defesa real é prévia pequena, marca d'água, original inacessível e limites de acesso. Bloquear o botão direito é cosmético. Alertar sobre acessos em massa.

---

## 11. Planos, cotas e custos de armazenamento

### Entitlements por plano (proposta; valores em D-12)
`storage_gb`, `max_members`, `albums_per_month`, recursos habilitados. As cotas são **verificadas no servidor** no momento do upload (nunca só na tela) e medidas em `studio_usage`.

### Custo de armazenamento (estimativa; confirmar nos sites oficiais antes de decidir)

Preços públicos consultados em 02/11/2026: Cloudflare R2 cerca de US$ 0,015 por GB-mês, sem cobrança de saída; Backblaze B2 cerca de US$ 6,95 por TB-mês, com saída grátis até 3× o armazenado.

| Cota de referência (planos Davions) | R2 (aprox./mês) | B2 (aprox./mês) |
|---|---|---|
| 100 GB | US$ 1,50 | US$ 0,70 |
| 500 GB | US$ 7,50 | US$ 3,50 |
| 1.000 GB | US$ 15,00 | US$ 7,00 |

Isso é **só armazenamento**. Somar: taxas de Pix/cartão, impostos, e-mail, WhatsApp (se houver), hospedagem, suporte e IA. Multiplicar pela cotação do dólar do dia.

### Trial
Referência: 30 dias sem cartão. Risco de abuso (contas descartáveis ocupando espaço). Proposta: cota reduzida no trial, verificação de e-mail, limites de upload, e **limpeza automática** após o fim do trial sem conversão (com aviso). Valores em D-14.

---

## 12. Álbuns (B3)

- O cliente seleciona as fotos; o sistema ordena por `taken_at` como sugestão.
- O diagramador reordena por arrastar e soltar, agrupa em lâminas e escolhe o tamanho, respeitando mínimo e máximo de páginas.
- A **ilustração** é a pré-visualização das lâminas com as prévias nas posições do layout.
- Estados: `draft` → `selecting` → `in_assembly` → `proof_sent` → `approved` → `delivered`. Transições validadas no servidor.
- Edição concorrente: salvamento automático com controle de versão.
- Exportação: ZIP numerado na ordem final + manifesto (CSV e PDF de conferência).
- **Diferencial a validar com fotógrafos reais** (hipóteses, não fatos): fluxo pensado para o **diagramador externo** (convite com acesso só àquele álbum), simplicidade, preço e Pix. O concorrente de referência já anuncia um diagramador de álbuns como "em breve".

---

## 13. Segurança

### Requisitos

| ID | Requisito | Tarefa |
|---|---|---|
| S-01 | Sessão opaca no servidor; cookie `HttpOnly`, `Secure`, `SameSite=Lax`; expiração curta e revogação | 006 |
| S-02 | argon2id; bloqueio progressivo após falhas | 006 |
| S-03 | 2FA TOTP obrigatório para donos de estúdio e admins da plataforma | 008 |
| S-04 | Rate limiting em login, link de acesso, download e formulários (por IP e por estúdio) | 006 |
| S-05 | RBAC (platform_admin, studio_owner, studio_member, assembler, client) | 007 |
| S-06 | Autorização **por recurso e por estúdio** em toda rota; testes de IDOR | 007 |
| S-07 | IDs públicos aleatórios (UUID) | 005 |
| S-08 | CSRF em ações que alteram dados | 006 |
| S-09 | CORS por `.env`, explícito | 003 |
| S-10 | Cabeçalhos de segurança no backend | 003 |
| S-11 | CSP, HSTS, `nosniff`, `frame-ancestors 'none'`, Referrer-Policy, Permissions-Policy no frontend | 004 |
| S-12 | Validação de toda entrada (Pydantic) e limite de corpo | 003 |
| S-13 | Somente consultas parametrizadas (ORM) | 005 |
| S-14 | Validação de upload por conteúdo, tipo, tamanho e limite de pixels | 010–011 |
| S-15 | Bucket privado, URLs assinadas curtas | 010 |
| S-16 | Webhooks (pagamento e assinatura) com assinatura verificada e idempotência | 016–017 |
| S-17 | Segredos só em variáveis de ambiente; varredura de segredos (gitleaks) | 004 |
| S-18 | Lockfiles versionados; `pip-audit` e `npm audit` no CI; Dependabot | 004 |
| S-19 | Next.js sempre na versão corrigida mais recente (houve falhas críticas em 2026; conferir o aviso vigente a cada atualização) | contínuo |
| S-20 | Erros sem stack trace; timeouts em chamadas externas | 003 |
| S-21 | Logs estruturados sem PII/segredos, com `request_id` e `studio_id` | 007 |
| S-22 | `audit_log` somente inserção | 007 |
| S-23 | Backups automáticos e **teste de restauração** | 019 |
| S-24 | TLS, HSTS, Cloudflare/WAF, firewall, SSH por chave | 019 |
| S-25 | Contêiner sem root; menor privilégio nos tokens de storage | 019 |
| S-26 | Revisão de segurança por **modelo diferente** do que escreveu o código | 036 |
| S-27 | Isolamento por estúdio: `studio_id` em tudo + RLS; papel do banco sem `BYPASSRLS` | 005, 007 |
| S-28 | Testes automáticos de isolamento entre estúdios em todas as rotas | 007 |
| S-29 | Storage com prefixo por estúdio; URL assinada só após checar estúdio | 010 |
| S-30 | Sites dos estúdios em domínio separado do app; CSP restritiva | 022 |
| S-31 | Sanitização de todo conteúdo escrito pelo estúdio (sem HTML cru) | 022 |
| S-32 | Slugs reservados; proteção contra tomada de subdomínio e domínio próprio verificado | 022, 029 |
| S-33 | Cotas e limites por estúdio (armazenamento, uploads, requisições) | 010, 016 |
| S-34 | Acesso de suporte da plataforma restrito, justificado e auditado | 007, 019 |

### Lacunas atuais
Sem autenticação/autorização; sem cabeçalhos; sem rate limiting; sem validação de upload; CORS permissivo (`allow_methods=["*"]`, `allow_headers=["*"]` com `allow_credentials=True`); sem logs/auditoria; frontend sem lockfile; sem SAST/Dependabot; LGPD não implementada; só HTTP local; sem multi-tenancy.

---

## 14. LGPD

> Guia técnico, não aconselhamento jurídico. **Um advogado deve revisar** termos de uso, política de privacidade, contrato de operador, autorização de imagem e política de conteúdo antes do beta com dados reais.

### Papéis
- **Fotógrafo/estúdio = controlador** dos dados dos clientes dele (inclusive fotos, e fotos de crianças).
- **Plataforma = operadora** desses dados: trata conforme as instruções do estúdio.
- **Plataforma = controladora** dos dados dos próprios fotógrafos (cadastro, cobrança, uso).

| ID | Requisito |
|---|---|
| L-01 | Termos de uso e **contrato de operador** (DPA) com cada estúdio no cadastro; lista de suboperadores (hospedagem, storage, e-mail, pagamento) |
| L-02 | Ferramentas para o estúdio cumprir a LGPD: registro de consentimentos, modelos de texto, exclusão e retenção configuráveis |
| L-03 | Fotos de **crianças e adolescentes**: consentimento específico e em destaque de ao menos um dos pais/responsável (art. 14), registrado em `consents` |
| L-04 | Autorização de uso de imagem para portfólio/redes **separada** da contratação |
| L-05 | Não usar **reconhecimento facial** (dado biométrico) |
| L-06 | Política de privacidade da plataforma, encarregado e canal de direitos do titular (`data_requests`) |
| L-07 | Retenção e eliminação automatizadas (prévias; originais conforme plano); exclusão sob pedido |
| L-08 | Minimização: dados de pagamento ficam com o provedor |
| L-09 | Registro das operações em `docs/lgpd/` e relatório de impacto quando aplicável |
| L-10 | **Incidente de segurança**: runbook pronto; prazo de 3 dias úteis para comunicar a ANPD e os titulares (em dobro para agentes de pequeno porte — verificar enquadramento); registro por 5 anos; definir em contrato o prazo para a operadora avisar o controlador |
| L-11 | Avaliar transferência internacional (storage, e-mail, IA fora do Brasil) |
| L-12 | **Conteúdo e abuso**: termos de uso, canal de denúncia e processo de remoção de conteúdo |
| L-13 | Acesso da equipe da plataforma aos dados dos estúdios: mínimo necessário e auditado (S-34) |
| L-14 | Cookies/analytics: consentimento só para itens não essenciais |

### Pagamentos (orientação jurídica e contábil necessária)
Usar provedor com **subcontas e divisão de pagamento**, para que o dinheiro do cliente final não fique retido na plataforma. Definir a cobrança das assinaturas (plataforma → estúdio) separada das vendas (cliente → estúdio). Consultar contador sobre impostos e notas.

---

## 15. Qualidade, processo com agentes e skills

- **Definição de pronto (DoD):** critérios de aceite atendidos; `ruff`, `mypy`, `pytest` verdes; `tsc`, ESLint e build do frontend verdes quando tocado; itens S-xx e L-xx da tarefa cumpridos e testados; **teste de isolamento entre estúdios** quando a tarefa criar ou alterar rotas; sem dependências novas sem aprovação; documentação atualizada; relatório em `docs/reviews/NNN-nome.md`; commit feito.
- **Testes por rota protegida:** sem login (401), papel errado (403), recurso de outro usuário ou **outro estúdio** (403/404), caso feliz.
- **CI:** lint, tipos, testes, `pip-audit`, `npm audit`, gitleaks, build.
- **Papéis dos agentes:** coordenador (planeja, escreve tarefas, revisa `git diff`), executor (`build`), explorador, revisor de segurança (somente leitura, modelo de outra família).
- Modelos gratuitos: só para código sem informação sensível.

### Ativação de skills e MCPs (só os que a tarefa listar)

| Quando | Skills/MCPs |
|---|---|
| 003–004 | Nenhum |
| 005–009 | `lgpd-data-mapping`, `lgpd-consent-schema`, `lgpd-dsar` (adaptar de Prisma para SQLAlchemy) |
| 019, 035 | `lgpd-audit` e demais skills de LGPD, com revisão jurídica |
| 021–022, 029 | `frontend-design`, web-interface-guidelines, GSAP (se aprovada), `chrome-devtools-mcp` (perfil isolado, sem telemetria), 21st MCP (somente busca) |
| 036 | `security-audit` (Cloudflare) com modelo forte e diferente |
| Nunca por padrão | `superpowers` (fluxos obrigatórios conflitam com este processo); só skills avulsas aprovadas: `test-driven-development`, `systematic-debugging`, `verification-before-completion` |

---

## 16. Roadmap

### Fase 0 — Fundação
- **003 Backend: reorganização + hardening base (sem Postgres).** `app/`; `core/config.py` (pydantic-settings); CORS por `.env`; middleware de cabeçalhos de segurança; limite de corpo e erros; `pyproject.toml` + ruff/mypy/pytest; `requirements-dev.txt`; venv Python 3.12/3.13; atualizar o pin do FastAPI; testes de `/health` e cabeçalhos; `.gitignore` ampliado.
- **004 Frontend e raiz.** Limpar boilerplate; estrutura `src/`; lockfile versionado; cabeçalhos no `next.config`; `.editorconfig`; `infra/docker-compose.yml` (PostgreSQL, MinIO, Mailpit — preparado); CI; Dependabot; gitleaks; ADR-001 a 008.
- **005 PostgreSQL + SQLAlchemy 2 + Alembic, já multi-tenant.** Engine/sessão; `studios`, `users`, `studio_members`, `sessions`, `audit_log`; `studio_id` em tudo; RLS e papel do banco sem `BYPASSRLS`; testes de integração em contêiner.

### Fase 1 — Identidade e acesso
- **006** Login (dono do estúdio e admin), sessão, logout, argon2id, bloqueio, rate limit, CSRF.
- **007** RBAC, autorização por recurso e por estúdio, **testes de isolamento**, `audit_log`, logging, acesso de suporte.
- **008** 2FA TOTP.
- **009** Acesso do cliente final (link mágico e/ou PIN — D-05) e consentimento inicial.

### Fase 2 — B1: galerias e fotos
- **010** Storage S3 (MinIO no dev), upload assinado, validações, `studio_usage` e cotas.
- **011** Worker de imagens: derivados, marca d'água, `taken_at`, limites.
- **012** CRUD de clientes e galerias, publicar, prazo configurável.
- **013** Galeria do cliente (API e tela) com a marca do estúdio, mobile first.
- **014** Favoritos, seleção e comentários.
- **015** Expiração das prévias e e-mails (acesso, lembrete, entrega).

### Fase 3 — B1: cobrança, pagamento e beta
- **016** Planos, assinatura e trial (cobrança da plataforma ao estúdio).
- **017** Pagamento do cliente final (Pix com split/subconta — D-01), webhook assinado e idempotente.
- **018** Liberação dos originais (URLs assinadas curtas) e registro de downloads.
- **019** **Pré-beta:** LGPD mínima (termos, privacidade, contrato de operador, direitos do titular, denúncia/remoção), revisão de segurança do que existe, backups com teste de restauração, ambiente de staging.
- **020** **Beta fechado** com 3 a 5 fotógrafos reais e **decisão de rumo** (o que entra no B2 e se o B3 sobe de prioridade).

### Fase 4 — B2: site e gestão do estúdio (épicos; ordem definida pelo beta)
- **021** Identidade visual e design system (referência: skill `frontend-design`).
- **022** Site do estúdio: construtor de páginas, tema, subdomínio, domínio separado do app.
- **023** CRM, clientes e Kanban.
- **024** Agenda e agendamento online.
- **025** Contratos e assinatura eletrônica (validade jurídica — D-17).
- **026** Briefing e questionários.
- **027** E-mails e WhatsApp automatizados (D-16).
- **028** Financeiro.
- **029** Domínio próprio e SEO.

### Fase 5 — B3: álbuns
- **030** Modelo de álbum, tamanhos e seleção do cliente.
- **031** Montagem: ordenação, lâminas, arrastar e soltar.
- **032** Ilustração do layout.
- **033** Prova, aprovação e exportação para produção.
- **034** Diagramador convidado e limites por plano.

> O beta pode indicar que o B3 deve vir antes do B2. A ordem das fases 4 e 5 é do Fagner.

### Fase 6 — Lançamento
- **035** LGPD operacional completa (retenção por estúdio, exportar/excluir, relatórios).
- **036** Revisão de segurança por modelo diferente, testes de abuso e de isolamento, auditoria de dependências, checklist OWASP ASVS.
- **037** Monitoramento, runbook de incidente, deploy de produção (VPS + Cloudflare), checklist de go-live.

---

## 17. Decisões pendentes (REQUEREM APROVAÇÃO do Fagner)

| ID | Decisão |
|---|---|
| D-01 | Provedor de Pix com subcontas/split (Mercado Pago, Asaas, Stripe etc.) |
| D-02 | Storage: Cloudflare R2 ou Backblaze B2 |
| D-03 | E-mail transacional |
| D-04 | Hospedagem, domínio da plataforma e domínio separado para sites dos estúdios |
| D-05 | Acesso do cliente final: link mágico, PIN ou ambos |
| D-06 | Tamanhos de álbum e regras de páginas (padrão da plataforma e/ou definido por estúdio) |
| D-07 | Retenção dos originais e prazo de download após pagamento, por plano |
| D-08 | Encarregado (nome e contato) e modelos de contrato/autorização de imagem |
| D-09 | shadcn/ui? Identidade visual da plataforma |
| D-10 | Diagramador: papel interno, convidado externo ou ambos |
| D-11 | Revisão jurídica: quem e quando (antes do beta com dados reais) |
| D-12 | Planos, preços e cotas |
| D-13 | Modelo de monetização: assinatura, comissão sobre vendas ou mista |
| D-14 | Trial: duração, cota, anti-abuso e limpeza |
| D-15 | Nome e marca (consultar advogado/INPI) |
| D-16 | WhatsApp: provedor e custos, ou só e-mail no início |
| D-17 | Contratos: assinatura eletrônica própria ou provedor; validade jurídica |

---

## 18. Riscos

| Risco | Mitigação |
|---|---|
| Um estúdio acessar dados de outro | `studio_id` + RLS + testes de isolamento em todas as rotas |
| Escopo gigante (concorrente maduro) | Três blocos; B1 como MVP; beta antes de B2 |
| Custo de armazenamento fora de controle | Cotas por plano, trial limitado, expiração, métricas por estúdio |
| Modelos gratuitos coletam dados | Dados fictícios; modelos pagos/zero retenção para código sensível |
| Falhas críticas no Next.js | Atualização contínua, Dependabot, contenção (sem root, tokens mínimos) |
| Pacotes inventados pela IA | Conferir nome/origem; instalação só com aprovação |
| XSS em conteúdo do estúdio | Sanitização, CSP restritiva, domínio separado |
| Vazamento de fotos | Bucket privado, URLs curtas, auditoria, rate limit |
| Questões legais (LGPD, pagamentos, abuso, marca) | Revisão jurídica e contábil antes do beta |
| Perda de dados | Backups e teste de restauração |

---

## 19. Glossário

- **Estúdio (tenant):** o espaço de um fotógrafo na plataforma.
- **Cliente final:** cliente do fotógrafo.
- **Prévia:** versão pequena e com marca d'água da foto, válida pelo prazo da galeria.
- **Original:** arquivo em alta qualidade, liberado após o pagamento.
- **Lâmina:** par de páginas do álbum.
- **Prova:** ilustração do álbum enviada ao cliente para aprovação.
- **RLS:** segurança por linha no PostgreSQL.
- **IDOR:** acessar o recurso de outra pessoa trocando um ID na URL.

---

## 20. Status (atualizar a cada tarefa)

| Tarefa | Descrição | Status |
|---|---|---|
| 001–002 | Etapas anteriores (ver `docs/tasks/`) | concluídas (confirmar) |
| 003 | Backend: reorganização + hardening base | pendente |
| 004 | Frontend e raiz | pendente |
| 005 | PostgreSQL + SQLAlchemy + Alembic multi-tenant | pendente |
| 006–009 | Identidade e acesso | pendente |
| 010–015 | B1: galerias e fotos | pendente |
| 016–020 | B1: cobrança, pagamento, pré-beta e beta | pendente |
| 021–029 | B2: site e gestão do estúdio | pendente |
| 030–034 | B3: álbuns | pendente |
| 035–037 | Lançamento | pendente |
