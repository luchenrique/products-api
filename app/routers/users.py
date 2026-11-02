from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.deps import require_roles
from app.models import Role, User
from app.routers.auth import user_out
from app.schemas import RoleUpdate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

manage = require_roles(*settings.split(settings.roles_users_manage))


@router.get("", response_model=list[UserOut], dependencies=[Depends(manage)])
def list_users(db: Session = Depends(get_db)):
    return [user_out(u) for u in db.scalars(select(User).order_by(User.id))]


@router.patch("/{user_id}/role", response_model=UserOut, dependencies=[Depends(manage)])
def change_role(user_id: int, data: RoleUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "Usuário não encontrado")
    role = db.scalar(select(Role).where(Role.name == data.role))
    if not role:
        raise HTTPException(422, f"Role '{data.role}' não existe")
    user.role_id = role.id
    db.commit()
    db.refresh(user)
    return user_out(user)
