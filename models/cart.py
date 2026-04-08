from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from datetime import datetime
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cart_item import CartItem


class Cart(Base):

    __tablename__ = "cart"
    __table_args__ = {"schema": "ecommerce"}

    id:Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("ecommerce.users.id"))

    created_at:Mapped[datetime] = mapped_column(server_default=func.now())

    updated_at:Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    items: Mapped[list["CartItem"]] = relationship("CartItem", lazy="noload")