from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from models import User
from typing import Annotated
from core import security
from schemas import CartItemAdd, CartItemResponse
from services import cart_item_service
from uuid import UUID

router = APIRouter(prefix="/cart-item", tags=["cart_items"])

@router.get("/", response_model=list[CartItemResponse])
async def get_items(current_user:Annotated[User, Depends(security.get_current_user)],db:AsyncSession = Depends(get_db)):
    try:
        return await cart_item_service.get_cart_items(current_user.id,db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=CartItemResponse, status_code= status.HTTP_201_CREATED)
async def add_item(data:CartItemAdd, current_user: Annotated[User, Depends(security.get_current_user)] ,db:AsyncSession = Depends(get_db)):
    try:
        return await cart_item_service.add_item(current_user.id,data, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(id:UUID, current_user: Annotated[User, Depends(security.get_current_user)], db:AsyncSession = Depends(get_db)):
    try:
        await cart_item_service.delete_item(current_user.id, id, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))