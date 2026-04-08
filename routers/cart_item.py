from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from models import User
from typing import Annotated
from core import security
from schemas import CartItemAdd, CartItemUpdateQty, CartResponse
from services import cart_item_service
from uuid import UUID

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=CartResponse)
async def get_cart(
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    return await cart_item_service.get_cart(current_user.id, db)


@router.post("/items", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def add_item(
    data: CartItemAdd,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    return await cart_item_service.add_item(current_user.id, data, db)


@router.put("/items/{item_id}", response_model=CartResponse)
async def update_item(
    item_id: UUID,
    data: CartItemUpdateQty,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    return await cart_item_service.update_item_quantity(current_user.id, item_id, data.quantity, db)


@router.delete("/items/{item_id}", response_model=CartResponse)
async def delete_item(
    item_id: UUID,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    return await cart_item_service.delete_item(current_user.id, item_id, db)


@router.delete("", response_model=CartResponse)
async def clear_cart(
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    return await cart_item_service.clear_cart(current_user.id, db)
