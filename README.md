# Volley Club Platform

![CI/CD](https://github.com/Agostinho-neto/k8s-volley-platform/actions/workflows/pipeline.yml/badge.svg)

API REST para gerenciamento de jogadores de vôlei com foco em arquitetura escalável e praticas de SRE.

## 🎯 Visão Geral

Plataforma backend para administração de clubes de vôlei. Gerencia cadastro, listagem e organização de jogadores com endpoints RESTful, validação de dados através de schemas Pydantic e containerização para deployment em qualquer ambiente.

## 🏗️ Stack Técnico

- **Framework**: FastAPI 0.136
- **Python**: 3.12-slim
- **Server**: Uvicorn ASGI
- **Validação**: Pydantic v2
- **Container**: Docker
- **Linting**: Ruff
- **Testing**: Pytest

## 🚀 Arquitetura

```
app/
├── main.py          # Entry point da aplicação
├── routes/          # Endpoints da API
│   └── players.py   # CRUD de jogadores
└── schemas/         # Modelos Pydantic
    └── player.py    # Schema Player
```

**Estrutura modular**: Separação clara entre routes, schemas e business logic facilita manutenção e testes.

## 📋 Endpoints

### Jogadores

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/players` | Criar novo jogador |
| GET | `/players` | Listar todos os jogadores |

**Request Body (POST):**
```json
{
  "name": "João Silva",
  "position": "Levantador",
  "number": 10
}
```

## 🐳 Docker

Imagem otimizada:

```dockerfile
FROM python:3.12-slim       # Base image leve
RUN pip install --no-cache  # Reduz tamanho
COPY . .                     # Cópia de código
CMD uvicorn app.main:app    # Execução
```

**Build e Run:**
```bash
docker build -t volleyops .
docker run -p 8000:8000 volleyops
```

## 💻 Desenvolvimento Local

### Requisitos
- Python 3.12+
- pip

### Setup

```bash
# Criar virtual environment
python -m venv venv

# Ativar (Windows)
.\venv\Scripts\Activate.ps1

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Executar servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse: http://localhost:8000/docs (Swagger UI)

### Testes

```bash
pytest
```

## 🔧 Práticas SRE Implementadas

✅ **Containerização**: Dockerfile otimizado para produção  
✅ **Versionamento**: Dependências congeladas em requirements.txt  
✅ **Linting**: Ruff para qualidade de código  
✅ **Validação**: Pydantic para data validation  
✅ **Modularidade**: Design pronto para escalabilidade  

## 📦 Dependências

Todas as dependências estão congeladas em `requirements.txt` com versões específicas para reprodutibilidade.

## 🔐 Variáveis de Ambiente

Suporte a `.env` via `python-dotenv` para configurações sensibles.

## 📈 Roadmap

- [ ] Health check endpoint (`/health`)
- [ ] Logging estruturado (JSON)
- [ ] Database integration (PostgreSQL)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Metrics e monitoring (Prometheus)
- [ ] Graceful shutdown handling


License

This project is licensed under the MIT License.