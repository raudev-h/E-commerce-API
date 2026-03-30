from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from core.database import get_db
from core import security
from schemas import  OrderResponse
from services import order_service
from uuid import UUID
from typing import Annotated


router = APIRouter(prefix="/order", tags=["orders"])

@router.get("/", response_model=list[OrderResponse])
async def get_orders(current_user:Annotated[User, Depends(security.get_current_user)], db:AsyncSession = Depends(get_db)):
    return await order_service.get_orders(current_user.id, db)


@router.get("/{id}", response_model=OrderResponse)
async def get_order(id:UUID, current_user:Annotated[User, Depends(security.get_current_user)], db:AsyncSession = Depends(get_db)):
    return await order_service.get_order(id,current_user.id,db)


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(current_user: Annotated[User, Depends(security.get_current_user)], db:AsyncSession = Depends(get_db)):
    return await order_service.create_order(current_user.id,db)


@router.patch("/{order_id}", response_model=OrderResponse)
async def cancel_order(current_user: Annotated[User, Depends(security.get_current_user)],order_id:UUID, db:AsyncSession = Depends(get_db)):
    return await order_service.cancel_order(current_user.id,order_id, db)
