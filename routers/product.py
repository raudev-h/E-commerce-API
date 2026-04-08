from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core import security
from models import User
from services import product_service
from schemas import ProductCreate, ProductUpdate, ProductResponse
from typing import Annotated
from uuid import UUID

router = APIRouter(prefix="/product", tags=["products"])


@router.get("", response_model=list[ProductResponse])
async def get_products(
    category_id: UUID | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    return await product_service.get_all_products(db, category_id, search, skip, limit)


@router.get("/{id}", response_model=ProductResponse)
async def get_product(id: UUID, db: AsyncSession = Depends(get_db)):
    return await product_service.get_product_by_id(id, db)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate,current_admin: Annotated[User, Depends(security.get_current_admin)], db: AsyncSession = Depends(get_db)):
    return await product_service.create_product(db, data)


@router.patch("/{id}", response_model=ProductResponse)
async def update_product(id:UUID, data:ProductUpdate, current_admin: Annotated[User, Depends(security.get_current_admin)],db:AsyncSession = Depends(get_db)):
    return await product_service.update_product(id, data, db) 


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id:UUID, current_admin: Annotated[User, Depends(security.get_current_admin)],db:AsyncSession = Depends(get_db)):
    await product_service.delete_product(id, db)