from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas import OrderCreate, OrderResponse
from services import order_service


router = APIRouter(prefix="/order", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(data:OrderCreate, db:AsyncSession = Depends(get_db)):
    try:
        return await order_service.create_order(data,db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))