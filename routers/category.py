from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from services import category_service
from uuid import UUID

router = APIRouter(prefix="/category", tags=["/category"])


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(db:AsyncSession = Depends(get_db)):
    return await category_service.get_all_categories(db)


@router.get("/{id}", response_model=CategoryResponse)
async def get_category(id:UUID, db:AsyncSession = Depends(get_db)):
    try:
        return await category_service.get_category_by_id(db, id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(data:CategoryCreate, db:AsyncSession = Depends(get_db)):
    try:
        return await category_service.create_category(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.patch("/{id}", response_model=CategoryResponse)
async def update_user(id:UUID, data:CategoryUpdate, db:AsyncSession = Depends(get_db)):
    try:
        return await category_service.update_category(id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))