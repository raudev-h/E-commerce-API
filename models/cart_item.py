from sqlalchemy import ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from uuid import UUID, uuid4


class CartItem(Base):

    __tablename__ = "cart_item"

    __table_args__ = (
        CheckConstraint("quantity > 0", name="quantity_non_negative"),
    )

    id:Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    cart_id:Mapped[UUID] = mapped_column(ForeignKey("cart.id"))

    product_id:Mapped[UUID] = mapped_column(ForeignKey("products.id"))

    quantity:Mapped[int] = mapped_column(Integer)