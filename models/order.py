from sqlalchemy import func, ForeignKey, Enum, Float, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from uuid import UUID, uuid4
from datetime import datetime
from typing import TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from .order_item import OrderItem


class Status(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "canceled"

class Order(Base):

    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint("total >= 0", name="total_non_negative"),
        {"schema": "ecommerce"}
    )

    id:Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    user_id:Mapped[UUID] = mapped_column(ForeignKey("ecommerce.users.id"))

    total:Mapped[float] = mapped_column(Float)

    created_at:Mapped[datetime] = mapped_column(server_default=func.now())

    updated_at:Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    status:Mapped[Status] = mapped_column(Enum(Status))

    items: Mapped[list["OrderItem"]] = relationship("OrderItem", lazy="noload")