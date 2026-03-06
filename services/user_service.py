from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User, Cart
from schemas import UserCreate, UserUpdateProfile
from uuid import UUID

async def get_all_users(db:AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return list(result.scalars().all())

async def get_user_by_id(db:AsyncSession, id:UUID) -> User:
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise ValueError("User not found")
    return user

async def create_user(db:AsyncSession, data:UserCreate) -> User:
    result = await db.execute(select(User).where(User.email == data.email))
    
    if result.scalar_one_or_none():
        raise ValueError(f"{data.email} already exists")
    
    user = User(
        first_name = data.first_name,
        last_name = data.last_name,
        email = data.email,
        password = data.password
    )
    db.add(user)
    await db.flush()

    cart = Cart(user_id = user.id)
    db.add(cart)
    await db.flush()
    
    return user

async def update_user_profle(db:AsyncSession, id:UUID, data:UserUpdateProfile) -> User:
    user = await get_user_by_id(db,id)
    updated_data = data.model_dump(exclude_unset=True)

    if not updated_data:
        return user

    for field, value in updated_data.items():
        setattr(user, field, value)

    await db.flush()
    await db.refresh(user)
    return user