from fastapi import APIRouter, HTTPException, status, Depends
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services import product_service
from schemas import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/product", tags=["products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(data:ProductCreate, db:AsyncSession = Depends(get_db)):
    try:
        return await product_service.create_product(db,data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))