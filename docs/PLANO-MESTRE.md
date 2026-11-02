# PLANO MESTRE — Pics (entrega de fotos e montagem de álbuns)

> Documento de referência para pessoas e agentes de IA. Leia inteiro antes de qualquer tarefa.
> Dono do produto e decisor final: **Fagner**. Versão 1 — 01/11/2026.
> Este arquivo é a fonte da verdade de escopo, arquitetura e regras. Ao concluir uma tarefa, atualize a seção 18 (Status).

---

## 0. Como usar este documento (regras para agentes)

1. Leia este plano e o `CLAUDE.md` antes de agir.
2. Trabalhe **uma tarefa por vez**, a partir de `docs/tasks/NNN-nome.md` (modelo em `docs/tasks/_modelo.md`).
3. Não saia do escopo da tarefa. Se achar algo fora do escopo, registre em `docs/reviews/` como observação e **não corrija por conta própria**.
4. Tudo que estiver marcado **REQUER APROVAÇÃO** (seção 15 e regras do `CLAUDE.md`) só avança com aprovação explícita do Fagner.
5. Use sempre **dados fictícios**. Nunca coloque fotos reais, dados de clientes, chaves ou `.env` em prompts, logs, testes ou commits. Modelos gratuitos podem coletar o que recebem.
6. Faça `git commit` antes e depois de cada tarefa. No máximo 2 rodadas de correção por tarefa; depois pare e consulte.
7. Antes de instalar qualquer pacote, confirme que o nome existe e é o oficial (modelos às vezes inventam nomes parecidos). Novas dependências **REQUEREM APROVAÇÃO**.
8. Nunca use o modo de aprovação automática (`--auto`).

---

## 1. Visão do produto

Uma empresa de fotografia terá:

- **Site institucional** (portfólio, serviços, contato) com visual premium.
- **Plataforma** por trás, para entrega de fotos e montagem de álbuns:
  - O fotógrafo (admin) sobe as fotos de um trabalho.
  - O cliente entra, vê **prévias de baixa qualidade** por **3 dias** e escolhe as fotos.
  - A seleção vira um **álbum**: fotos em ordem, formato/tamanho definidos e uma **ilustração visual** do layout, para quem monta o álbum ter facilidade.
  - Após o **pagamento**, o cliente recebe os arquivos em alta qualidade.

### Restrições do projeto

- **Custo baixo**: usar camadas gratuitas e serviços baratos; planos gratuitos de IA só com dados fictícios.
- **Segurança forte** desde o início (seção 11).
- **LGPD** como requisito de projeto, não como acabamento (seção 12).
- **Visual extraordinário** no site e nas áreas logadas (seção 14, fase 5).
- Desenvolvimento assistido por IA (OpenCode com DeepSeek e outros, Claude Code), portanto tarefas pequenas, revisáveis e com critérios de aceite claros.

---

## 2. Perfis e fluxo principal

| Perfil | Papel no sistema |
|---|---|
| Visitante | Navega no site institucional, envia contato |
| Cliente (`client`) | Acessa a galeria, favorita e seleciona fotos, aprova prova do álbum, paga, baixa |
| Montador (`assembler`) | Organiza o álbum a partir da seleção do cliente e exporta para produção |
| Admin (`admin`) | Gerencia clientes, galerias, prazos, álbuns, pedidos e usuários |

**Fluxo:**

1. Admin cria o cliente e a galeria, faz upload em lote. O sistema gera as prévias.
2. Admin publica a galeria. O cliente recebe o acesso por e-mail. Contagem de 3 dias começa.
3. Cliente vê as prévias, favorita e seleciona as fotos do álbum.
4. A seleção alimenta o álbum. O montador ajusta a ordem, o tamanho e as lâminas, e gera a ilustração.
5. Cliente aprova a prova do álbum.
6. Cliente paga (Pix).
7. O sistema libera os originais (links assinados e curtos) e registra os downloads.
8. Prévias expiram e são apagadas. Originais seguem a política de retenção (decisão D-07).

---

## 3. Requisitos funcionais

**Admin**
- RF-01 Cadastrar e gerenciar clientes e usuários internos.
- RF-02 Criar galerias; upload em lote de fotos (JPEG/PNG), com progresso e retomada.
- RF-03 Publicar e despublicar galeria; prazo das prévias padrão de 3 dias, configurável e prorrogável (com registro).
- RF-04 Ver favoritas e seleção do cliente por galeria.
- RF-05 Gerenciar tamanhos de álbum (dimensões, mínimo e máximo de páginas, preço).
- RF-06 Acompanhar pedidos e pagamentos; liberar entrega.

**Cliente**
- RF-07 Acessar a galeria por link/credencial segura.
- RF-08 Ver prévias (com marca d'água) em grade e em tela cheia, no celular e no desktop.
- RF-09 Favoritar fotos e montar a seleção do álbum.
- RF-10 Aprovar ou pedir ajustes na prova do álbum.
- RF-11 Pagar via Pix e acompanhar o status.
- RF-12 Baixar os originais após a confirmação do pagamento.
- RF-13 Solicitar acesso, correção ou exclusão dos próprios dados (LGPD).

**Montador**
- RF-14 Ver a seleção do cliente já ordenada (sugestão pelo horário da foto).
- RF-15 Reordenar por arrastar e soltar; organizar em lâminas.
- RF-16 Escolher o tamanho do álbum e ver a ilustração do layout.
- RF-17 Exportar o pacote para produção (ZIP numerado + manifesto CSV/PDF).

**Site**
- RF-18 Home, portfólio, serviços, sobre, contato.
- RF-19 Política de privacidade e termos de uso.
- RF-20 Formulário de contato protegido contra robôs.

---

## 4. Requisitos não funcionais

- **Segurança**: seção 11. **LGPD**: seção 12.
- **Desempenho**: upload direto ao storage (não passa pelo servidor); processamento de imagem fora da requisição; prévias leves; paginação e miniaturas.
- **Mobile first**: o cliente escolhe fotos pelo celular.
- **Acessibilidade**: WCAG AA (contraste, teclado, `prefers-reduced-motion`).
- **Idioma**: pt-BR. Datas em America/Fortaleza ou configurável; armazenar em UTC.
- **Dinheiro**: sempre em centavos (inteiro), nunca float.
- **Observabilidade**: logs estruturados com id de requisição, sem dados pessoais nem segredos.
- **Custo**: monitorar armazenamento e tráfego de saída; preferir storage sem cobrança de saída.

---

## 5. Arquitetura

```
Navegador ──► Frontend (Next 16) ──► API (FastAPI) ──► PostgreSQL
                                        │
                                        ├──► Storage S3-compatível PRIVADO (originais, prévias)
                                        ├──► Worker de imagens (derivados + marca d'água)
                                        ├──► E-mail transacional
                                        └──► Provedor de Pix (webhook assinado)
```

### Stack

| Camada | Escolha |
|---|---|
| Backend | Python 3.12 ou 3.13 (evitar 3.14 por compatibilidade), FastAPI, Pydantic v2, pydantic-settings |
| Banco | PostgreSQL, SQLAlchemy 2, Alembic |
| Auth | Sessão opaca no servidor + cookie `HttpOnly`; senha com argon2id; 2FA TOTP para admin |
| Imagens | Pillow (ou pyvips), em worker |
| Storage | S3-compatível privado (Cloudflare R2 ou Backblaze B2; MinIO no desenvolvimento) via boto3 e URLs assinadas |
| Tarefas | Começar com rotina agendada e fila simples; evoluir para fila dedicada se necessário |
| Frontend | Next 16, TypeScript estrito, Tailwind; shadcn/ui **REQUER APROVAÇÃO** |
| Qualidade | ruff, mypy, pytest, ESLint, `tsc`, CI no GitHub Actions |
| Infra local | Docker Compose: PostgreSQL, MinIO, Mailpit |

### Decisões a registrar em `docs/adr/` (status: proposta até aprovação)

- ADR-001 Frontend e backend separados (Next + FastAPI).
- ADR-002 PostgreSQL + SQLAlchemy 2 + Alembic.
- ADR-003 Sessão opaca no servidor com cookie `HttpOnly` (revogável), em vez de JWT.
- ADR-004 Storage privado com URLs assinadas; original nunca público.
- ADR-005 Processamento de imagem em worker com limites de tamanho.
- ADR-006 Dinheiro em centavos; webhooks idempotentes.

### Comunicação frontend e backend

Em produção, usar o mesmo "site" (ex.: `app.dominio` e `api.dominio`) com cookie `SameSite=Lax`, `Secure`, `HttpOnly`. Ações que alteram dados exigem proteção contra CSRF (token por sessão + verificação de `Origin`). CORS com origens e métodos explícitos, vindo do `.env`, nunca `*` com credenciais.

---

## 6. Estado atual (01/11/2026)

```
pics/
├─ backend/    main.py (tudo em 1 arquivo), requirements.txt, .env.example
├─ frontend/   Next 16 boilerplate (src/app, public com SVGs do template)
├─ docs/       tasks/, reviews/, _modelo.md
├─ .opencode/  skills locais
├─ CLAUDE.md, README.md, opencode.json, .gitignore
```

### Problemas de organização

**Backend:** `main.py` único (sem rotas, config, banco e schemas separados); sem `tests/`, `alembic/`, `pyproject.toml`; sem `requirements-dev.txt`; CORS e versão hardcoded; `python-dotenv` instalado e não usado.
**Frontend:** boilerplate (SVGs do template, README duplicado); sem `components/`, `lib/`, `hooks/`, `types/`, `services/`; `package.json` com `name: "frontend"` e **sem lockfile versionado**.
**Raiz:** sem `infra/docker-compose.yml`, `.editorconfig`, CI e `docs/adr/`; `.gitignore` não cobre `.venv/`, `dist/`, `coverage/`, `.pytest_cache/`, `.ruff_cache/`.
**Ambiente:** FastAPI global (0.141.1) diverge do pin (0.115.6). **Atualizar o pin para a versão validada em teste, em vez de rebaixar a global** (pins antigos perdem correções de segurança). Usar venv. Python 3.14 é novo demais: usar 3.12 ou 3.13.

### Segurança: o que já existe

CORS restrito a `localhost:3000`; `.env` fora do Git; `.env.example` só com placeholders; agentes proibidos de ler `.env` (`opencode.json`); versões fixas no backend; TypeScript strict + ESLint; sem `dangerouslySetInnerHTML` nem segredos no cliente.

---

## 7. Estrutura alvo

```
backend/
├─ app/
│  ├─ main.py
│  ├─ api/v1/{router.py, deps.py, routes/{health,auth,galleries,photos,albums,orders,webhooks}.py}
│  ├─ core/{config.py, security.py, logging.py}
│  ├─ db/{base.py, session.py}
│  ├─ models/  schemas/  repositories/
│  ├─ services/{storage.py, images.py, mail.py, payments.py, ...}
│  └─ workers/{process_photo.py, expire_galleries.py}
├─ alembic/
├─ tests/{conftest.py, unit/, integration/}
└─ pyproject.toml  requirements.txt  requirements-dev.txt  .env.example
frontend/src/{app/, components/{ui,layout}, lib/, hooks/, types/, services/}
infra/docker-compose.yml        # PostgreSQL, MinIO, Mailpit
docs/{adr/, tasks/, reviews/, lgpd/}
.github/workflows/ci.yml  .github/dependabot.yml  .editorconfig
```

---

## 8. Modelo de dados (proposta — validar antes da migração)

PostgreSQL, chaves `uuid`, datas `timestamptz` (UTC), dinheiro em centavos.

| Tabela | Campos principais |
|---|---|
| `users` | id, email (citext único), password_hash (nulo p/ cliente), role (`admin`/`assembler`/`client`), full_name, is_active, totp_secret (criptografado), created_at, last_login_at |
| `sessions` | id, user_id, token_hash, created_at, expires_at, revoked_at, user_agent |
| `magic_links` | id, user_id, gallery_id (opcional), token_hash, expires_at, used_at |
| `galleries` | id, client_id, title, event_date, status (`draft`/`published`/`expired`/`closed`), published_at, preview_expires_at, created_by |
| `photos` | id, gallery_id, original_key, sha256, width, height, size_bytes, **taken_at** (do EXIF, lido antes de remover), sort_index, status (`uploaded`/`processing`/`ready`/`failed`) |
| `photo_derivatives` | id, photo_id, kind (`thumb`/`preview`), storage_key, width, height |
| `favorites` | client_id, photo_id, created_at (PK composta) |
| `album_sizes` | id, name, width_mm, height_mm, min_pages, max_pages, price_cents, active |
| `albums` | id, gallery_id, size_id, status (`draft`/`selecting`/`in_assembly`/`proof_sent`/`approved`/`delivered`), approved_at, notes |
| `album_spreads` | id, album_id, position, layout |
| `album_items` | id, album_id, spread_id, photo_id, position, crop (jsonb) |
| `orders` | id, gallery_id, client_id, status (`pending`/`paid`/`canceled`/`refunded`), total_cents, created_at |
| `payments` | id, order_id, provider, provider_ref (único), status, amount_cents, paid_at |
| `webhook_events` | id, provider, event_id (único), payload_hash, received_at, processed_at |
| `downloads` | id, user_id, gallery_id, photo_id, at, ip_hash |
| `consents` | id, user_id, purpose (`delivery`/`portfolio`/`marketing`), is_minor_data, guardian_name, text_version, granted_at, revoked_at |
| `data_requests` | id, user_id, type (`access`/`correction`/`deletion`), status, opened_at, closed_at |
| `audit_log` | id, actor_id, action, entity, entity_id, at, ip_hash, meta (jsonb); **somente inserção** |

Índices em chaves estrangeiras e em `(gallery_id, sort_index)`. Restrições de unicidade e checagem no banco, não só na aplicação.

---

## 9. Fotos: proteção e ciclo de vida

**Upload**
1. O cliente do upload (admin) pede à API uma URL assinada de envio. A API valida papel, cota, tipo e tamanho.
2. O arquivo vai direto ao bucket privado, com chave aleatória.
3. A API "finaliza" e enfileira o processamento.

**Processamento (worker)**
- Verificar o tipo pelo conteúdo real do arquivo (não pela extensão); aceitar só JPEG e PNG.
- Abrir com limite de pixels (proteção contra "bomba de descompressão") e tamanho máximo.
- Ler `taken_at` do EXIF, corrigir a orientação e **remover o EXIF** dos derivados (pode conter GPS).
- Gerar `thumb` (~400 px) e `preview` (lado maior ≤ ~1200 px, JPEG de qualidade moderada) com **marca d'água diagonal repetida** contendo o código da galeria.
- Nomes de objeto aleatórios. Marcar a foto como `ready` ou `failed`.

**Entrega**
- O **original nunca chega ao navegador antes do pagamento confirmado**.
- Prévias e miniaturas via URL assinada de poucos minutos, emitida só após checar permissão (cliente é dono da galeria, galeria publicada e não expirada).
- Após o pagamento, downloads por URL assinada curta, com registro em `downloads`.
- Não usar o otimizador de imagens do Next para fotos de clientes.

**Expiração**
- `preview_expires_at = published_at + PREVIEW_TTL_DAYS` (padrão 3).
- Rotina agendada apaga prévias e miniaturas vencidas e marca a galeria como `expired`. Aviso por e-mail 1 dia antes.
- Prorrogação pelo admin fica registrada no `audit_log`.
- Retenção dos **originais** é separada do prazo das prévias (decisão D-07).

**Limitação assumida**: não é possível impedir 100% de capturas de tela. A defesa real é prévia pequena, marca d'água, original inacessível e limites de acesso. Bloquear o botão direito é apenas cosmético. Alertar sobre downloads/requisições em massa.

---

## 10. Álbuns

- O cliente seleciona as fotos; o sistema ordena por `taken_at` como sugestão inicial.
- O montador reordena por arrastar e soltar, agrupa em lâminas e escolhe o tamanho (`album_sizes`), respeitando mínimo e máximo de páginas.
- A **ilustração** do álbum é uma pré-visualização das lâminas com as prévias nas posições do layout.
- Estados: `draft` → `selecting` → `in_assembly` → `proof_sent` → `approved` → `delivered`. Transições validadas no servidor.
- Edição concorrente: salvamento automático com controle de versão (evitar que dois montadores se sobrescrevam).
- Exportação: ZIP com arquivos numerados na ordem final + manifesto (CSV e PDF de conferência).

---

## 11. Segurança

### Requisitos

| ID | Requisito | Tarefa |
|---|---|---|
| S-01 | Sessão opaca no servidor; cookie `HttpOnly`, `Secure`, `SameSite=Lax`; expiração curta e revogação | 006 |
| S-02 | Senhas com argon2id; bloqueio progressivo após falhas | 006 |
| S-03 | 2FA TOTP obrigatório para admin | 008 |
| S-04 | Rate limiting em login, link de acesso, download e formulários | 006 |
| S-05 | RBAC (admin/assembler/client) | 007 |
| S-06 | Autorização **por recurso** (dono da galeria) em toda rota + testes de IDOR para cada rota | 007 |
| S-07 | IDs públicos aleatórios (UUID); nunca sequenciais | 005 |
| S-08 | CSRF em ações que alteram dados | 006 |
| S-09 | CORS por `.env`, origens/métodos/cabeçalhos explícitos | 003 |
| S-10 | Cabeçalhos de segurança no backend | 003 |
| S-11 | CSP, HSTS, `nosniff`, `frame-ancestors 'none'`, Referrer-Policy e Permissions-Policy no frontend | 004 |
| S-12 | Validação de toda entrada (Pydantic) e limite de tamanho do corpo | 003 |
| S-13 | Somente consultas parametrizadas (ORM); nenhum SQL por concatenação | 005 |
| S-14 | Validação de upload por conteúdo, tipo e tamanho; limite de pixels | 010–011 |
| S-15 | Bucket privado e URLs assinadas curtas | 010 |
| S-16 | Webhook de pagamento com assinatura verificada e idempotência | 018 |
| S-17 | Segredos só em variáveis de ambiente; varredura de segredos (gitleaks) | 004 |
| S-18 | Lockfiles versionados; `pip-audit` e `npm audit` no CI; Dependabot | 004 |
| S-19 | Next.js sempre na versão corrigida mais recente (houve falhas críticas de execução remota em 2026; conferir o aviso vigente a cada atualização) | contínuo |
| S-20 | Erros sem stack trace para o cliente; timeouts em chamadas externas | 003 |
| S-21 | Logs estruturados sem PII/segredos; id de requisição | 007 |
| S-22 | `audit_log` somente inserção (logins, downloads, ações de admin) | 007 |
| S-23 | Backups automáticos e **teste de restauração** | 025 |
| S-24 | TLS, HSTS, Cloudflare/WAF na frente, firewall (portas 80/443), SSH por chave | 025 |
| S-25 | Contêiner sem root e menor privilégio nos tokens de storage | 025 |
| S-26 | Revisão de segurança por **modelo diferente** do que escreveu o código | 024 |

### Lacunas atuais

Sem autenticação/autorização; sem cabeçalhos de segurança; sem rate limiting; sem validação de upload; CORS permissivo (`allow_methods=["*"]`, `allow_headers=["*"]` com `allow_credentials=True`); sem logs/auditoria; frontend sem lockfile; sem SAST/Dependabot; LGPD não implementada; só HTTP local.

---

## 12. LGPD

> Isto é um guia técnico, não aconselhamento jurídico. **Um advogado deve revisar** política de privacidade, termos, contrato e autorização de imagem antes do lançamento.

| ID | Requisito |
|---|---|
| L-01 | Definir a **base legal por finalidade**: entrega do serviço (execução de contrato), uso no portfólio e marketing (consentimento próprio, separado e revogável) |
| L-02 | Fotos de **crianças e adolescentes**: consentimento específico e em destaque de ao menos um dos pais/responsável (art. 14), registrado em `consents` |
| L-03 | Autorização de uso de imagem para portfólio/redes **separada** da contratação |
| L-04 | Não usar **reconhecimento facial** (dado biométrico) |
| L-05 | Política de privacidade, termos de uso e aviso claro de prazos de retenção |
| L-06 | **Encarregado** (contato de privacidade) e canal para direitos do titular (acesso, correção, exclusão) com `data_requests` |
| L-07 | Retenção e eliminação automatizadas (prévias em 3 dias; originais conforme política D-07); exclusão sob pedido |
| L-08 | Minimização: não coletar dado que não seja necessário (dados de pagamento ficam com o provedor) |
| L-09 | Registro das operações de tratamento em `docs/lgpd/` e relatório de impacto quando aplicável |
| L-10 | **Incidente de segurança**: runbook pronto; comunicação à ANPD e aos titulares em **3 dias úteis** (prazo em dobro para agentes de pequeno porte — verificar enquadramento); manter registro por 5 anos |
| L-11 | Contratos/termos com operadores (hospedagem, storage, e-mail, pagamento); avaliar transferência internacional de dados |
| L-12 | Cookies/analytics: só pedir consentimento se usar itens não essenciais |

---

## 13. Qualidade e processo com agentes

- **Definição de pronto (DoD)** de toda tarefa: critérios de aceite atendidos; `ruff`, `mypy` e `pytest` verdes; `tsc`, ESLint e build do frontend verdes quando tocado; itens S-xx e L-xx da tarefa cumpridos e testados; sem novas dependências sem aprovação; documentação atualizada; relatório em `docs/reviews/NNN-nome.md`; commit feito.
- **Testes obrigatórios** por rota protegida: sem login (401), papel errado (403), recurso de outro usuário (404/403), caso feliz.
- **CI** (`.github/workflows/ci.yml`): lint, tipos, testes, `pip-audit`, `npm audit`, gitleaks, build.
- **Papéis dos agentes**: coordenador (planeja, escreve tarefas, revisa `git diff`), executor (`build`), explorador (lê o projeto), revisor de segurança (somente leitura, modelo de outra família).
- Modelos gratuitos: só para código sem informação sensível.

---

## 14. Roadmap

### Fase 0 — Fundação
- **003 Backend: reorganização + hardening base (sem Postgres).** Mover para `app/`; `core/config.py` com pydantic-settings lendo `.env`; CORS por `.env` e restrito; middleware de cabeçalhos de segurança; limite de corpo e tratamento de erros; `pyproject.toml` + ruff/mypy/pytest; `requirements-dev.txt`; venv com Python 3.12/3.13; atualizar o pin do FastAPI; testes de `/health` e dos cabeçalhos; `.gitignore` ampliado.
- **004 Frontend e raiz.** Remover boilerplate; estrutura `src/`; renomear pacote; versionar lockfile; cabeçalhos de segurança no `next.config`; `.editorconfig`; `infra/docker-compose.yml` (PostgreSQL, MinIO, Mailpit — preparado, sem subir); CI; Dependabot; gitleaks (pre-commit); ADR-001 a 006.
- **005 PostgreSQL + SQLAlchemy 2 + Alembic.** Sessão/engine, `Base`, primeira migração (`users`, `sessions`, `audit_log`), testes de integração com PostgreSQL em contêiner.

> A tarefa 003 original cobria backend, frontend e raiz juntos. Foi dividida em 003 e 004 para manter tarefas pequenas e revisáveis.

### Fase 1 — Identidade e acesso
- **006** Login do admin (seed por CLI), sessão, logout, argon2id, bloqueio progressivo, rate limit, CSRF.
- **007** RBAC, autorização por recurso, testes de IDOR, `audit_log`, logging com id de requisição.
- **008** 2FA TOTP para admin e recuperação.
- **009** Acesso do cliente (link mágico de uso único e/ou PIN — decisão D-05) e consentimento inicial.

### Fase 2 — Galerias e fotos
- **010** Storage S3 (MinIO no dev), upload assinado e validações.
- **011** Worker de imagens: derivados, marca d'água, `taken_at`, limites.
- **012** CRUD de galerias (admin), publicar, prazo de 3 dias.
- **013** Galeria do cliente (API e tela): grade, tela cheia, favoritos.
- **014** Rotina de expiração e e-mails de lembrete.

### Fase 3 — Álbuns
- **015** Modelo de álbum, tamanhos e seleção do cliente.
- **016** Montagem: ordenação, lâminas, ilustração do layout.
- **017** Prova e aprovação do cliente; exportação para o montador.

### Fase 4 — Pagamento
- **018** Pedido + Pix (provedor D-01) + webhook assinado e idempotente.
- **019** Liberação dos originais (URLs assinadas curtas + registro de downloads).

### Fase 5 — Site e identidade visual (pode começar após a 013)
- **020** Briefing visual, design tokens e layout base (usar a skill `frontend-design`).
- **021** Páginas: home, portfólio, serviços, sobre, contato.
- **022** Áreas logadas (admin e cliente) com a mesma identidade; acessibilidade e desempenho.

### Fase 6 — LGPD operacional e pré-lançamento
- **023** Páginas legais, consentimentos finais, direitos do titular (exportar/excluir), retenção.
- **024** Revisão de segurança por modelo diferente, testes de abuso, auditoria de dependências, checklist OWASP ASVS.
- **025** Backups com teste de restauração, monitoramento, runbook de incidente, deploy (VPS + Cloudflare), checklist de go-live.

---

## 15. Decisões pendentes (REQUEREM APROVAÇÃO do Fagner)

| ID | Decisão |
|---|---|
| D-01 | Provedor de Pix (Mercado Pago, Asaas, Stripe etc.) |
| D-02 | Storage: Cloudflare R2 ou Backblaze B2 |
| D-03 | E-mail transacional (Resend, SMTP próprio etc.) |
| D-04 | Hospedagem (VPS, PaaS) e domínio/subdomínios |
| D-05 | Acesso do cliente: link mágico, PIN ou ambos |
| D-06 | Tamanhos de álbum, preços e regras de páginas |
| D-07 | Retenção dos originais e prazo de download após pagamento |
| D-08 | Encarregado (nome e contato) e modelo de autorização de imagem |
| D-09 | Usar shadcn/ui? Identidade visual e referências do site |
| D-10 | Montador é papel separado ou permissão do admin? |
| D-11 | Revisão jurídica: quem e quando |

---

## 16. Riscos

| Risco | Mitigação |
|---|---|
| Modelos gratuitos coletam dados | Dados fictícios; modelos pagos/zero retenção para código sensível |
| Falhas críticas no Next.js | Atualização contínua, Dependabot, contenção (sem root, tokens mínimos) |
| Pacotes inventados pela IA | Conferir nome/origem antes de instalar; instalação só com aprovação |
| Limites de cota de modelos gratuitos | Tarefas pequenas, poucos agentes, um modelo por função |
| Vazamento de fotos | Bucket privado, URLs curtas, auditoria, rate limit |
| Perda de dados | Backups e teste de restauração |
| Escopo crescendo | Uma tarefa por vez, critérios de aceite, fora de escopo explícito |
| Custo de storage/tráfego | Storage sem cobrança de saída, expiração das prévias, monitoramento |

---

## 17. Glossário

- **Prévia**: versão pequena e com marca d'água da foto, válida por 3 dias.
- **Original**: arquivo em alta qualidade, liberado só após o pagamento.
- **Lâmina**: par de páginas do álbum.
- **Prova**: ilustração do álbum enviada ao cliente para aprovação.
- **IDOR**: acessar o recurso de outra pessoa trocando um ID na URL.

---

## 18. Status (atualizar a cada tarefa)

| Tarefa | Descrição | Status |
|---|---|---|
| 001–002 | Etapas anteriores (ver `docs/tasks/`) | concluídas |
| 003 | Backend: reorganização + hardening base | concluída (inclui hardening 003B) |
| 003B | Hardening restante e atualização de pins | concluída |
| 003C | Agentes, skills, MCPs e permissões | pendente de correção: configuração não atende os critérios de aceite |
| 004 | Frontend e raiz | pendente |
| 005 | PostgreSQL + SQLAlchemy + Alembic | pendente |
| 006–009 | Identidade e acesso | pendente |
| 010–014 | Galerias e fotos | pendente |
| 015–017 | Álbuns | pendente |
| 018–019 | Pagamento | pendente |
| 020–022 | Site e identidade visual | pendente |
| 023–025 | LGPD operacional e pré-lançamento | pendente |
