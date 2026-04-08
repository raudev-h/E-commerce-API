from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from models import CartItem, User, Product, Cart
from schemas import CartItemAdd
from core import NotFoundException, BadRequestException, ConflictException
from uuid import UUID


async def get_cart(user_id: UUID, db: AsyncSession) -> Cart:
    cart = await db.execute(
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
    )
    cart = cart.scalar_one_or_none()
    if not cart:
        raise NotFoundException("cart not found")
    return cart


async def get_cart_items(user_id: UUID, db: AsyncSession) -> list[CartItem]:
    cart = await db.execute(select(Cart).where(Cart.user_id == user_id))
    cart = cart.scalar_one_or_none()
    if not cart:
        raise NotFoundException("user not found")
    items = await db.execute(select(CartItem).where(CartItem.cart_id == cart.id))
    return list(items.scalars().all())


async def add_item(user_id: UUID, item: CartItemAdd, db: AsyncSession) -> Cart:
    user = await db.execute(select(User).where(User.id == user_id))
    if not user.scalar_one_or_none():
        raise NotFoundException("user not found")

    product = await db.execute(
        select(Product).where(Product.id == item.product_id, Product.is_active == True)
    )
    product = product.scalar_one_or_none()
    if not product:
        raise NotFoundException("product not found")

    cart = await db.execute(select(Cart).where(Cart.user_id == user_id))
    cart = cart.scalar_one_or_none()
    if not cart:
        raise NotFoundException("cart not found")

    existing = await db.execute(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == item.product_id,
        )
    )
    existing = existing.scalar_one_or_none()

    total_qty = (existing.quantity + item.quantity) if existing else item.quantity
    _unavailable_stock(product.stock, total_qty, f"not enough stock for {product.name}")

    if existing:
        existing.quantity += item.quantity
        await db.flush()
    else:
        db.add(CartItem(cart_id=cart.id, product_id=item.product_id, quantity=item.quantity))
        await db.flush()

    return await get_cart(user_id, db)


async def update_item_quantity(user_id: UUID, item_id: UUID, quantity: int, db: AsyncSession) -> Cart:
    cart = await db.execute(select(Cart).where(Cart.user_id == user_id))
    cart = cart.scalar_one_or_none()
    if not cart:
        raise NotFoundException("cart not found")

    item = await db.execute(
        select(CartItem).where(CartItem.id == item_id, CartItem.cart_id == cart.id)
    )
    item = item.scalar_one_or_none()
    if not item:
        raise NotFoundException("cart item not found")

    product = await db.execute(select(Product).where(Product.id == item.product_id))
    product = product.scalar_one_or_none()
    _unavailable_stock(product.stock, quantity, f"not enough stock for {product.name}")

    item.quantity = quantity
    await db.flush()

    return await get_cart(user_id, db)


async def delete_item(user_id: UUID, item_id: UUID, db: AsyncSession) -> Cart:
    cart = await db.execute(select(Cart).where(Cart.user_id == user_id))
    cart = cart.scalar_one_or_none()
    if not cart:
        raise NotFoundException("cart not found")

    item = await db.execute(
        select(CartItem).where(CartItem.id == item_id, CartItem.cart_id == cart.id)
    )
    item = item.scalar_one_or_none()
    if not item:
        raise NotFoundException("cart item not found")

    await db.delete(item)
    await db.flush()

    return await get_cart(user_id, db)


async def clear_cart(user_id: UUID, db: AsyncSession) -> Cart:
    cart = await db.execute(select(Cart).where(Cart.user_id == user_id))
    cart = cart.scalar_one_or_none()
    if not cart:
        raise NotFoundException("cart not found")

    items = await db.execute(select(CartItem).where(CartItem.cart_id == cart.id))
    for item in items.scalars().all():
        await db.delete(item)
    await db.flush()

    return await get_cart(user_id, db)


def _unavailable_stock(product_stock: int, item_quantity: int, message: str):
    if product_stock < item_quantity:
        raise BadRequestException(message)
