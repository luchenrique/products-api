from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select

from app import database, models
from app.config import settings
from app.routers import auth, products, users
from app.security import hash_password

ROLES = ["admin", "manager", "viewer"]


def seed(db) -> None:
    """Cria as roles e o usuário admin inicial, se ainda não existirem."""
    for name in ROLES:
        if not db.scalar(select(models.Role).where(models.Role.name == name)):
            db.add(models.Role(name=name))
    db.commit()
    if not db.scalar(select(models.User).where(models.User.email == settings.admin_email)):
        admin = db.scalar(select(models.Role).where(models.Role.name == "admin"))
        db.add(
            models.User(
                email=settings.admin_email,
                hashed_password=hash_password(settings.admin_password),
                role_id=admin.id,
            )
        )
        db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.Base.metadata.create_all(bind=database.engine)
    with database.SessionLocal() as db:
        seed(db)
    yield


app = FastAPI(title="Products API", version="1.0.0", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
