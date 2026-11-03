# Tarefa 004B - Configurar Docker local

## Objetivo
Preparar o ambiente Windows para usar Docker Compose no desenvolvimento do Pics e validar a configuração local de PostgreSQL, MinIO e Mailpit, sem iniciar containers.

## Contexto
- A tarefa 004 preparou `infra/docker-compose.yml` e `.env.example`, mas a validação `docker compose config` ficou pendente.
- Diagnóstico deste ambiente: Docker Desktop não instalado; comando `docker` ausente; WSL não instalado; `VirtualizationFirmwareEnabled` reportado como `False`; sessão atual sem privilégios de administrador.
- O processador é AMD Ryzen 5 5500; a opção de virtualização costuma aparecer no firmware como SVM/AMD-V.

## Critérios de aceite
- [x] Virtualização necessária ao WSL 2 está operacional; o kernel do Docker Desktop confirma WSL2.
- [x] WSL 2 operacional (`docker-desktop` em execução, versão 2).
- [x] Docker Desktop usa o backend WSL 2 (`desktop-linux`).
- [x] `docker version`, `docker compose version` e `docker info` executam sem erro após iniciar o Docker Desktop.
- [x] `docker compose --env-file .env.example -f infra/docker-compose.yml config` valida PostgreSQL, MinIO e Mailpit.
- [x] Nenhum container ou imagem foi iniciado/baixado nesta tarefa; `docker ps --all` e `docker image ls` estão vazios.
- [x] Atualizar `docs/RETOMADA.md` e revisar `docs/reviews/004B-configurar-docker-local.md`.

## Arquivos que podem ser alterados
- `docs/tasks/004B-configurar-docker-local.md`
- `docs/reviews/004B-configurar-docker-local.md`
- `docs/RETOMADA.md`

## Fora de escopo
- Ativar virtualização ou alterar opções de firmware sem ação manual de Fagner.
- Instalar Docker Desktop sem privilégios administrativos.
- Executar `docker compose up`, baixar imagens ou iniciar os serviços do Pics.
- Alterar `infra/docker-compose.yml`, dependências do projeto ou qualquer `.env`.

## Regras de segurança aplicáveis
- Não ler nem registrar valores de `.env`; usar somente `.env.example` fictício.
- Manter serviços expostos apenas em loopback, conforme o Compose do projeto.
- Não iniciar serviços nem fazer mudanças persistentes no ambiente sem os pré-requisitos.

## Como testar
1. Conferir `wsl --status` e `wsl --list --verbose`.
2. Conferir `docker version`, `docker compose version` e `docker info`.
3. Executar `docker compose --env-file .env.example -f infra/docker-compose.yml config` sem `up`.
4. Executar `git diff --check`.

## Relatório do executor (preenchido pelo OpenCode)
- O que foi feito: Docker Desktop existente foi iniciado; WSL2 confirmou backend operacional. A configuração Compose foi validada com `.env.example`, sem iniciar containers ou baixar imagens.
- Arquivos alterados: `docs/tasks/004B-configurar-docker-local.md`, `docs/reviews/004B-configurar-docker-local.md` e `docs/RETOMADA.md`.
- Dúvidas ou riscos: nenhuma pendência ambiental identificada para o uso local do Docker Compose.
