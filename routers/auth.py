from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core import security
from schemas import Token, UserCreate, UserResponse
from services import user_service
from typing import Annotated
from datetime import timedelta


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:AsyncSession = Depends(get_db)) -> Token:
    user = await user_service.autenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={"sub":str(user.id), "role": user.role.value, "first_name": user.first_name}, expires_delta=access_token_expires)

    return Token(access_token=access_token)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(db, data)