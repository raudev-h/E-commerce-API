from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas import UserCreate, UserUpdateProfile, UserResponse
from services import user_service
from uuid import UUID

router = APIRouter(prefix="/user", tags=["/user"])


@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await user_service.get_all_users(db)


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        return await user_service.get_user_by_id(db, id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={str(e)})


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await user_service.create_user(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={str(e)})


@router.patch("/{id}", response_model=UserResponse)
async def update_user_profile(
    id: UUID, data: UserUpdateProfile, db: AsyncSession = Depends(get_db)):
    try:
        return await user_service.update_user_profle(db, id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
