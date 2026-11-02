# Products API

API REST de CRUD de produtos com **FastAPI**, **PostgreSQL**, autenticação por **token JWT** e controle de acesso por **roles**.

## Tecnologias
- Python 3.12  
- FastAPI 
- SQLAlchemy 2 
- PostgreSQL 16 
- PyJWT + bcrypt 
- Pytest 
- Docker / Docker Compose

## Estrutura
```
app/
  main.py        # app, lifespan, seed de roles e admin
  config.py      # settings (.env), incluindo roles por endpoint
  database.py    # engine / sessão
  models.py      # Role, User, Product
  schemas.py     # Pydantic
  security.py    # hash de senha e JWT
  deps.py        # get_current_user e require_roles(...)
  routers/       # auth, users, products
tests/           # pytest (SQLite em memória)
```

## Rodando tudo com Docker (API + Postgres)
```bash
cp .env.example .env
docker compose up --build
```
- API: http://localhost:8000 · Docs (Swagger): http://localhost:8000/docs
- Health check: `curl http://localhost:8000/health`

## Rodando a API localmente (só o banco no Docker)
```bash
cp .env.example .env
docker compose up -d db
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Testes
```bash
pytest -v
```
Os testes usam SQLite em memória (não precisam do Postgres) e trocam a dependência `get_db`.

## Autenticação
1. `POST /auth/register` — cria usuário com a role `viewer`.
2. `POST /auth/login` (form: `username` = e-mail, `password`) — retorna `access_token`.
3. Envie `Authorization: Bearer <token>` nas demais rotas.

Admin inicial (criado no startup): `admin@admin.com` / `admin123` (configurável no `.env`).

## Permissões (roles)
Roles no banco: `admin`, `manager`, `viewer`. Cada recurso tem suas roles permitidas, parametrizadas no `.env`:

| Recurso | Variável | Padrão |
|---|---|---|
| `GET /products`, `GET /products/{id}` | `ROLES_PRODUCTS_READ` | admin, manager, viewer |
| `POST`, `PUT`, `PATCH /products` | `ROLES_PRODUCTS_WRITE` | admin, manager |
| `DELETE /products/{id}` | `ROLES_PRODUCTS_DELETE` | admin |
| `GET /users`, `PATCH /users/{id}/role` | `ROLES_USERS_MANAGE` | admin |

Sem token → `401`. Role sem permissão → `403`.

## Endpoints
| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/register` | Cadastro |
| POST | `/auth/login` | Login (JWT) |
| GET | `/auth/me` | Usuário logado |
| POST | `/products` | Criar produto |
| GET | `/products?skip=&limit=&name=` | Listar (paginação e filtro) |
| GET | `/products/{id}` | Detalhar |
| PUT | `/products/{id}` | Substituir |
| PATCH | `/products/{id}` | Atualizar parcialmente |
| DELETE | `/products/{id}` | Remover |
| GET | `/users` | Listar usuários (admin) |
| PATCH | `/users/{id}/role` | Alterar role (admin) |

