from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from services import category_service
from uuid import UUID

router = APIRouter(prefix="/category", tags=["/category"])

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(data:CategoryCreate, db:AsyncSession = Depends(get_db)):
    try:
        return await category_service.create_category(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))