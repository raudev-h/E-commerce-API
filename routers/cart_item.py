from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas import CartItemAdd, CartItemResponse
from services import cart_item_service
from uuid import UUID

router = APIRouter(prefix="/cart-item", tags=["cart_items"])

@router.get("/", response_model=list[CartItemResponse])
async def get_items(user_id:UUID,db:AsyncSession = Depends(get_db)):
    try:
        return await cart_item_service.get_cart_items(user_id,db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=CartItemResponse, status_code= status.HTTP_201_CREATED)
async def add_item(data:CartItemAdd, db:AsyncSession = Depends(get_db)):
    try:
        return await cart_item_service.add_item(data, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(id:UUID, db:AsyncSession = Depends(get_db)):
    try:
        await cart_item_service.delete_item(id,db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))