from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Order, OrderItem, Cart, CartItem, User, Product
from models.order import Status
from core import BadRequestException, NotFoundException, ConflictException
from uuid import UUID


async def get_orders(user_id:UUID, db:AsyncSession):
    user = await db.execute(select(User).where(User.id == user_id))

    if not user.scalar_one_or_none():
        raise NotFoundException("user not found")
    
    orders = await db.execute(select(Order).where(Order.user_id == user_id))

    orders = orders.scalars().all()

    return list(orders)

async def get_order(order_id:UUID, user_id:UUID, db:AsyncSession):
    user = await db.execute(select(User).where(User.id == user_id))

    if not user.scalar_one_or_none():
        raise NotFoundException("user not found")
    
    order = await db.execute(select(Order).where(Order.id == order_id, Order.user_id == user_id))

    order = order.scalar_one_or_none()

    if not order:
        raise NotFoundException("order not found")

    return order

async def create_order(user_id:UUID, db:AsyncSession) -> Order:
    user = await db.execute(select(User).where(User.id == user_id, User.is_active))

    if not user.scalar_one_or_none():
        raise NotFoundException("user not found")
    
    items = await _get_all_items(user_id, db)

    order = Order(
            user_id=user_id,
            status=Status.PENDING,
            total=0
        )
    db.add(order)
    await db.flush()

    total_price = 0

    product_ids = [item.product_id for item in items]

    products = await db.execute(select(Product).where(Product.id.in_(product_ids)))

    products = {p.id:p for p in products.scalars().all()}

    for item in items:
        product = products[item.product_id]
        
        order_item = OrderItem(
            order_id= order.id,
            product_id = product.id,
            quantity = item.quantity,
            unit_price = product.price
        )

        product.stock -= item.quantity
        order_item_price = product.price * item.quantity

        total_price += order_item_price

        await db.delete(item)

        db.add(order_item)

    order.total = total_price
    await db.flush()
    await db.refresh(order)

    return order

async def cancel_order(order_id:UUID, db:AsyncSession):
    cancellable_statuses = [Status.PENDING, Status.CONFIRMED]

    order = await _get_order_by_id(order_id, db)
    
    if not order.status in cancellable_statuses:
        raise BadRequestException("order cannot be cancelled")

    order.status = Status.CANCELLED

    await db.flush()
    await db.refresh(order)

    return order

async def _get_all_items(id:UUID, db:AsyncSession):
    cart = await db.execute(select(Cart).where(Cart.user_id == id))

    cart = cart.scalar_one_or_none()

    if not cart:
        raise NotFoundException("user not found")
    
    cart_items = await db.execute(select(CartItem).where(CartItem.cart_id == cart.id))

    cart_items = cart_items.scalars().all()

    if not cart_items:
        raise ConflictException("empty cart")

    return list(cart_items)

async def _get_order_by_id(order_id:UUID, db:AsyncSession) -> Order:
    order = await db.execute(select(Order).where(Order.id == order_id))

    order = order.scalar_one_or_none()

    if not order:
        raise NotFoundException("order not found")
    
    return order
