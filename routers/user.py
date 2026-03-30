from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core import security
from models import User
from schemas import UserCreate, UserUpdateProfile, UserResponse
from services import user_service
from typing import Annotated
from uuid import UUID

router = APIRouter(prefix="/user", tags=["/user"])


@router.get("/", response_model=list[UserResponse])
async def get_users(current_admin: Annotated[User, Depends(security.get_current_admin)],db: AsyncSession = Depends(get_db)):
        return await user_service.get_all_users(db)


@router.get("/{id}", response_model=UserResponse)
async def get_user(current_admin: Annotated[User, Depends(security.get_current_admin)],id: UUID, db: AsyncSession = Depends(get_db)):
    return await user_service.get_user_by_id(db, id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(db, data)


@router.patch("/{id}", response_model=UserResponse)
async def update_user_profile(
    id: UUID, data: UserUpdateProfile, db: AsyncSession = Depends(get_db)):
    return await user_service.update_user_profle(db, id, data)