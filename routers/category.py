from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core import security
from models import User
from schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from services import category_service
from typing import Annotated
from uuid import UUID

router = APIRouter(prefix="/category", tags=["/category"])


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(db:AsyncSession = Depends(get_db)):
    return await category_service.get_all_categories(db)


@router.get("/{id}", response_model=CategoryResponse)
async def get_category(id:UUID, db:AsyncSession = Depends(get_db)):
    return await category_service.get_category_by_id(db, id)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(data:CategoryCreate, current_admin: Annotated[User, Depends(security.get_current_admin)], db:AsyncSession = Depends(get_db)):
    return await category_service.create_category(db, data)


@router.patch("/{id}", response_model=CategoryResponse)
async def update_user(id:UUID, data:CategoryUpdate, current_admin: Annotated[User, Depends(security.get_current_admin)], db:AsyncSession = Depends(get_db)):
    return await category_service.update_category(id, data, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id:UUID, current_admin: Annotated[User, Depends(security.get_current_admin)] ,db:AsyncSession = Depends(get_db)):
    await category_service.delete_category(id, db)
