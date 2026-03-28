from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from core.database import get_db
from core import security
from schemas import  OrderResponse
from services import order_service
from core import NotFoundException, BadRequestException, ConflictException
from uuid import UUID
from typing import Annotated


router = APIRouter(prefix="/order", tags=["orders"])

@router.get("/", response_model=list[OrderResponse])
async def get_orders(current_user:Annotated[User, Depends(security.get_current_user)], db:AsyncSession = Depends(get_db)):
    try:
        return await order_service.get_orders(current_user.id, db)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{id}", response_model=OrderResponse)
async def get_order(id:UUID, current_user:Annotated[User, Depends(security.get_current_user)], db:AsyncSession = Depends(get_db)):
    try:
        return await order_service.get_order(id,current_user.id,db)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(current_user: Annotated[User, Depends(security.get_current_user)], db:AsyncSession = Depends(get_db)):
    try:
        return await order_service.create_order(current_user.id,db)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
@router.patch("/{order_id}", response_model=OrderResponse)
async def cancel_order(order_id:UUID, db:AsyncSession = Depends(get_db)):
    try:
        return await order_service.cancel_order(order_id, db)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))