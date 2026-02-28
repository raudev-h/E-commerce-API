from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Category
from schemas import CategoryCreate, CategoryUpdate
from uuid import UUID


async def get_all_categories(db:AsyncSession) -> list[Category]:
    result = await db.execute(select(Category))
    return list(result.scalars().all())

async def get_category_by_id(db:AsyncSession, id:UUID) -> Category:
    result = await db.execute(select(Category).where(Category.id == id))
    category = result.scalar_one_or_none()
    
    if not category:
        raise ValueError("category not found")
    
    return category

async def create_category(db:AsyncSession, data:CategoryCreate) -> Category:
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