# Backend: configuração do banco

O backend usa SQLAlchemy 2, o driver Psycopg 3 e Alembic. `DATABASE_URL` deve ser
definida no ambiente do processo; a aplicação e as migrações não leem `.env`.
Não imprima esse valor nem o inclua em logs ou relatórios.

## Dependências

Com Python 3.12 e o ambiente virtual do backend ativado:

```powershell
python -m pip install -r requirements.txt -r requirements-dev.txt
```

## PostgreSQL local e migrações

Use uma instância PostgreSQL local descartável e um banco de teste chamado
`pics_test`. O Compose publica o serviço somente em loopback. Inicie apenas o
PostgreSQL e aguarde o healthcheck:

```powershell
$env:POSTGRES_DB = 'pics_test'
docker compose --env-file .env.example -p pics-task005 -f ../infra/docker-compose.yml up -d postgres
docker compose --env-file .env.example -p pics-task005 -f ../infra/docker-compose.yml ps postgres
```

Defina `DATABASE_URL` no ambiente do terminal com os parâmetros sintéticos da
instância local, sem exibi-la. Com o diretório atual em `backend/`, execute:

```powershell
alembic upgrade head
pytest
ruff check app tests
mypy app
```

Os testes de integração são ignorados quando a variável não está definida; se
estiver definida, exigem PostgreSQL, host local ou de serviço de CI e o banco
específico `pics_test`. A rotina testa migração, persistência, unicidade de
email sem distinção de caixa, hash de sessão único, validação do papel no banco
e rejeição de `UPDATE`/`DELETE` em `audit_log`. A limpeza remove as tabelas de
teste por downgrade e reaplica a migração; não apaga registros de auditoria
diretamente. Para remover o serviço e seu volume descartável:

```powershell
docker compose --env-file .env.example -p pics-task005 -f ../infra/docker-compose.yml down -v
```
