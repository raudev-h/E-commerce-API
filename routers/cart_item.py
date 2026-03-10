from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas import CartItemAdd, CartItemUpdate, CartItemResponse
from services import cart_item_service
from uuid import UUID

router = APIRouter(prefix="/cart-item", tags=["cart_items"])

@router.post("/", response_model=CartItemResponse, status_code= status.HTTP_201_CREATED)
async def add_item(data:CartItemAdd, db:AsyncSession = Depends(get_db)):
    try:
        return await cart_item_service.add_item(data, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))