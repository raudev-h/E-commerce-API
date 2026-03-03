from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Product, Category
from schemas import ProductCreate, ProductUpdate
from uuid import UUID


async def get_all_products(db: AsyncSession, category_id:UUID | None = None, skip:int = 0, limit:int = 10) -> list[Product]:
    if category_id:
        result = await db.execute(select(Product).where(Product.category_id == category_id))
        return list(result.scalars().all())[skip:skip + limit]
    result = await db.execute(select(Product))
    return list(result.scalars().all())


async def get_product_by_id(id: UUID, db: AsyncSession) -> Product:
    result = await db.execute(
        select(Product).where(Product.id == id, Product.is_active == True)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise ValueError("Product not found")
    return product


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
