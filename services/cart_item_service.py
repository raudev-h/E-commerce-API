from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import CartItem, User, Product, Cart
from schemas import CartItemAdd, CartItemUpdate
from uuid import UUID

async def add_item(item:CartItemAdd, db:AsyncSession) -> CartItem:     
    user = await db.execute(select(User).where(User.id == item.user_id))
    user = user.scalar_one_or_none()

    if not user:
        raise ValueError("user not found")
    
    product = await db.execute(select(Product).where(Product.id == item.product_id, Product.is_active))

    product = product.scalar_one_or_none()

    if not product:
        raise ValueError("product not found")

    cart = await db.execute(select(Cart).where(Cart.user_id == item.user_id))
    cart = cart.scalar_one_or_none()

    if not cart:
        raise ValueError("cart not found")
    
    existent_cart_item = await db.execute(select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == item.product_id))

    existent_cart_item = existent_cart_item.scalar_one_or_none()
    
    total = existent_cart_item.quantity + item.quantity if existent_cart_item else item.quantity

    _unavailable_stock(product.stock, total,f"not enough stock for {product.name}")
    
    if existent_cart_item:    
        existent_cart_item.quantity += item.quantity
        await db.flush()
        await db.refresh(existent_cart_item)
        return existent_cart_item

    cart_item = CartItem(cart_id = cart.id, product_id = item.product_id, quantity = item.quantity)
    
    db.add(cart_item)
    await db.flush()
    await db.refresh(cart_item)
    return cart_item

async def delete_item(id:UUID, db:AsyncSession) -> None:
    cart_item = await db.execute(select(CartItem).where(CartItem.id == id))

    cart_item = cart_item.scalar_one_or_none()

    if not cart_item:
        raise ValueError("cart item not found")

    await db.delete(cart_item)
    await db.flush()

def _unavailable_stock(product_stock:int, item_quantity:int, message:str):
    if product_stock < item_quantity:
        raise ValueError(message)
