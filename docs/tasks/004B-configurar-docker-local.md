# Tarefa 004B - Configurar Docker local

## Objetivo
Preparar o ambiente Windows para usar Docker Compose no desenvolvimento do Pics e validar a configuração local de PostgreSQL, MinIO e Mailpit, sem iniciar containers.

## Contexto
- A tarefa 004 preparou `infra/docker-compose.yml` e `.env.example`, mas a validação `docker compose config` ficou pendente.
- Diagnóstico deste ambiente: Docker Desktop não instalado; comando `docker` ausente; WSL não instalado; `VirtualizationFirmwareEnabled` reportado como `False`; sessão atual sem privilégios de administrador.
- O processador é AMD Ryzen 5 5500; a opção de virtualização costuma aparecer no firmware como SVM/AMD-V.

## Critérios de aceite
- [ ] Virtualização AMD (SVM/AMD-V) habilitada no firmware/BIOS.
- [ ] WSL 2 instalado e operacional em sessão com privilégios de administrador.
- [ ] Docker Desktop instalado e configurado para usar o backend WSL 2, ou runtime Docker equivalente aprovado.
- [ ] `docker version`, `docker compose version` e `docker info` executam sem erro.
- [ ] `docker compose --env-file .env.example -f infra/docker-compose.yml config` valida PostgreSQL, MinIO e Mailpit.
- [ ] Não iniciar containers nem baixar imagens nesta tarefa.
- [ ] Atualizar `docs/RETOMADA.md` e criar revisão em `docs/reviews/004B-configurar-docker-local.md`.

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
- O que foi feito:
- Arquivos alterados:
- Dúvidas ou riscos:
