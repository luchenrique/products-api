from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    stock: int = Field(default=0, ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    """PATCH parcial: todos os campos opcionais."""

    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str


class RoleUpdate(BaseModel):
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
