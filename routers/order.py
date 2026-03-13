from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas import OrderCreate, OrderResponse
from services import order_service
from uuid import UUID


router = APIRouter(prefix="/order", tags=["orders"])

@router.get("/", response_model=list[OrderResponse])
async def get_orders(user_id:UUID, db:AsyncSession = Depends(get_db)):
    try:
        return await order_service.get_orders(user_id, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
@router.get("/{id}", response_model=OrderResponse)
async def get_order(id:UUID, user_id:UUID, db:AsyncSession = Depends(get_db)):
    try:
        return await order_service.get_order(id,user_id,db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(data:OrderCreate, db:AsyncSession = Depends(get_db)):
    try:
        return await order_service.create_order(data,db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{order_id}", response_model=OrderResponse)
async def cancel_order(order_id:UUID, db:AsyncSession = Depends(get_db)):
    try:
        return await order_service.cancel_order(order_id, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))