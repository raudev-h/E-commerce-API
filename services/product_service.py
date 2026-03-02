from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Product, Category
from schemas import ProductCreate, ProductUpdate
from uuid import UUID


async def create_product(db: AsyncSession, data: ProductCreate) -> Product:
    result = await db.execute(
        select(Category).where(
            Category.id == data.category_id, Category.is_active == True
        )
    )

    if not result.scalar_one_or_none():
        raise ValueError("Category not found")

    result = await db.execute(
        select(Product).where(Product.name == data.name, Product.is_active == True)
    )

    if result.scalar_one_or_none():
        raise ValueError(f"Product: {data.name} already exist")

    product = Product(**data.model_dump())

    db.add(product)
    await db.flush()

    return product
