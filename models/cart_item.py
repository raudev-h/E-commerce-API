from sqlalchemy import ForeignKey, Integer, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from uuid import UUID, uuid4
from datetime import datetime


class CartItem(Base):

    __tablename__ = "cart_item"

    __table_args__ = (
        CheckConstraint("quantity > 0", name="quantity_non_negative"),
        {"schema": "ecommerce"}

    )

    id:Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    cart_id:Mapped[UUID] = mapped_column(ForeignKey("ecommerce.cart.id"))

    product_id:Mapped[UUID] = mapped_column(ForeignKey("ecommerce.products.id"))

    quantity:Mapped[int] = mapped_column(Integer)

    updated_at:Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())