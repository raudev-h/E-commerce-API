from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Category
from schemas import CategoryCreate, CategoryUpdate
from uuid import UUID

async def create_category(db:AsyncSession, data:CategoryCreate):
    result = await db.execute(select(Category).where(Category.name == data.name))

    if result.scalar_one_or_none():
        raise ValueError(f"Category: {data.name} already exists")
    
    category = Category(
        name = data.name,
        description = data.description
    )

    db.add(category)
    await db.flush()
    return category