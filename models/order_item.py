from sqlalchemy import ForeignKey, Float, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from uuid import UUID, uuid4
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product

class OrderItem(Base):

    __tablename__ = "order_items"
    __table_args__ = {"schema": "ecommerce"}

    id:Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    order_id:Mapped[UUID] = mapped_column(ForeignKey("ecommerce.orders.id"))

    product_id:Mapped[UUID] = mapped_column(ForeignKey("ecommerce.products.id"))

    quantity:Mapped[int] = mapped_column(Integer)

    unit_price:Mapped[float] = mapped_column(Float)

    created_at:Mapped[datetime] = mapped_column(server_default=func.now())

    product: Mapped["Product"] = relationship("Product", lazy="noload")