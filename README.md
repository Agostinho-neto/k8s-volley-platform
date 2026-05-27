# Volley Club Platform

![CI/CD](https://github.com/Agostinho-neto/k8s-volley-platform/actions/workflows/pipeline.yml/badge.svg)

Aplicacao web e API REST para gerenciamento de jogadores de volei com foco em arquitetura escalavel e praticas de SRE.

## Visao Geral

Plataforma para administracao de clubes de volei. Gerencia cadastro, listagem, alteracao e remocao de jogadores com interface web, endpoints RESTful, validacao de dados com schemas Pydantic, persistencia em banco relacional e containerizacao para execucao local ou deployment em ambientes orquestrados.

## Stack Tecnico

- **Framework**: FastAPI 0.136
- **Python**: 3.12-slim
- **Server**: Uvicorn ASGI
- **Validacao**: Pydantic v2
- **ORM**: SQLAlchemy 2
- **Database**: PostgreSQL
- **Migrations**: Alembic
- **Container**: Docker e Docker Compose
- **Linting**: Ruff
- **Testing**: Pytest
- **CI/CD**: GitHub Actions
- **Frontend**: HTML, CSS e JavaScript

## Arquitetura

```text
app/
|-- main.py              # Entry point da aplicacao
|-- database.py          # Engine, session e dependencia de banco
|-- models/              # Models SQLAlchemy
|   `-- player.py        # Tabela players
|-- repositories/        # Acesso ao banco de dados
|   `-- player.py        # Queries de jogadores
|-- routes/              # Endpoints da API
|   `-- players.py       # Rotas de jogadores
|-- static/              # Interface web
|   |-- index.html       # Tela de gerenciamento
|   |-- styles.css       # Estilos da interface
|   `-- app.js           # Consumo da API via fetch
`-- schemas/             # Modelos Pydantic
    `-- player.py        # Schemas de entrada e saida

alembic/
`-- versions/            # Migrations versionadas do banco
```

**Estrutura modular**: Separacao entre routes, schemas, models, repositories e database facilita manutencao, testes e evolucao para uma aplicacao mais proxima de producao.

## Endpoints

### Web

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| GET | `/` | Interface web da aplicacao |
| GET | `/docs` | Swagger UI da API |

### Jogadores

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| POST | `/players` | Criar novo jogador |
| GET | `/players` | Listar todos os jogadores |
| GET | `/players/{player_id}` | Buscar jogador por ID |
| PUT | `/players/{player_id}` | Alterar jogador |
| DELETE | `/players/{player_id}` | Remover jogador |

**Request Body (POST/PUT):**

```json
{
  "name": "Joao Silva",
  "position": "Levantador",
  "number": 10
}
```

**Response:**

```json
{
  "id": 1,
  "name": "Joao Silva",
  "position": "Levantador",
  "number": 10,
  "created_at": "2026-05-15T19:57:22",
  "updated_at": "2026-05-15T19:57:22"
}
```

## Docker

Imagem otimizada:

```dockerfile
FROM python:3.12-slim
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD uvicorn app.main:app
```

**Build e Run:**

```bash
docker build -t volleyops .
docker run -p 8000:8000 volleyops
```

## Docker Compose

O projeto possui `docker-compose.yml` com API e PostgreSQL.

```bash
docker compose up --build
```

O Compose executa as migrations com Alembic antes de subir a API.

Acesse:

```text
http://localhost:8000
http://localhost:8000/docs
```

## Desenvolvimento Local

### Requisitos

- Python 3.12+
- pip
- Docker e Docker Compose

### Setup

```bash
# Criar virtual environment
python -m venv venv

# Ativar (Windows)
.\venv\Scripts\Activate.ps1

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Variaveis de Ambiente

Copie o exemplo de ambiente:

```bash
cp .env.example .env
```

Exemplo:

```env
DATABASE_URL=postgresql://volleyops:volleyops@localhost:5432/volleyops
```

### Migrations

Aplicar migrations:

```bash
alembic upgrade head
```

Criar uma nova migration apos alterar models:

```bash
alembic revision --autogenerate -m "describe change"
```

### Executar Servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse:

```text
http://localhost:8000
http://localhost:8000/docs
```

### Testes

```bash
pytest
```

### Lint

```bash
ruff check .
```

## CI/CD

O workflow em `.github/workflows/pipeline.yml` executa:

- Checkout do repositorio
- Setup do Python 3.12
- Instalacao de dependencias
- PostgreSQL como service container
- Ruff
- Alembic migrations
- Pytest
- Build da imagem Docker
- Push da imagem para Docker Hub

## Praticas SRE Implementadas

- **Containerizacao**: Dockerfile para empacotar a aplicacao
- **Ambiente local reproduzivel**: Docker Compose com API e PostgreSQL
- **Versionamento de banco**: Alembic para migrations
- **Persistencia relacional**: PostgreSQL com SQLAlchemy
- **CRUD completo**: Criacao, leitura, atualizacao e remocao de jogadores
- **Interface web**: Tela simples para operar a API
- **Versionamento de dependencias**: `requirements.txt` com versoes especificas
- **Linting**: Ruff para qualidade de codigo
- **Validacao**: Pydantic para data validation
- **CI/CD**: GitHub Actions com banco em pipeline
- **Modularidade**: Separacao entre rotas, schemas, models e repositories
- **Logging estruturado**: logs em JSON no stdout com request ID, rota, status code e latencia

## Dependencias

Todas as dependencias estao congeladas em `requirements.txt` com versoes especificas para reprodutibilidade.

## Roadmap

- [ ] Health check endpoint (`/health`)
- [ ] Readiness check com validacao de banco (`/ready`)
- [x] Logging estruturado (JSON)
- [x] Database integration (PostgreSQL)
- [x] CI/CD pipeline (GitHub Actions)
- [ ] Metrics e monitoring (Prometheus)
- [ ] Dashboards de observabilidade
- [ ] Graceful shutdown handling
- [ ] Kubernetes manifests

## License

This project is licensed under the MIT License.
