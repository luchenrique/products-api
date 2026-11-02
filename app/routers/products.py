from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.deps import require_roles
from app.models import Product
from app.schemas import ProductCreate, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])

can_read = require_roles(*settings.split(settings.roles_products_read))
can_write = require_roles(*settings.split(settings.roles_products_write))
can_delete = require_roles(*settings.split(settings.roles_products_delete))


def get_or_404(db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto não encontrado")
    return product


@router.post(
    "", response_model=ProductOut, status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(can_write)],
)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("", response_model=list[ProductOut], dependencies=[Depends(can_read)])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    name: str | None = Query(None, description="Filtro por nome (contém)"),
    db: Session = Depends(get_db),
):
    stmt = select(Product).order_by(Product.id).offset(skip).limit(limit)
    if name:
        stmt = stmt.where(Product.name.ilike(f"%{name}%"))
    return db.scalars(stmt).all()


@router.get("/{product_id}", response_model=ProductOut, dependencies=[Depends(can_read)])
def get_product(product_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, product_id)


@router.put("/{product_id}", response_model=ProductOut, dependencies=[Depends(can_write)])
def replace_product(product_id: int, data: ProductCreate, db: Session = Depends(get_db)):
    product = get_or_404(db, product_id)
    for key, value in data.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@router.patch("/{product_id}", response_model=ProductOut, dependencies=[Depends(can_write)])
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    product = get_or_404(db, product_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete(
    "/{product_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(can_delete)]
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db.delete(get_or_404(db, product_id))
    db.commit()
