from sqlalchemy import ForeignKey, Float, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from uuid import UUID, uuid4
from datetime import datetime

class OrderItem(Base):

    __tablename__ = "order_items"

    id:Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    order_id:Mapped[UUID] = mapped_column(ForeignKey("orders.id"))

    product_id:Mapped[UUID] = mapped_column(ForeignKey("products.id"))

    quantity:Mapped[int] = mapped_column(Integer)

    unit_price:Mapped[float] = mapped_column(Float)

    created_at:Mapped[datetime] = mapped_column(server_default=func.now())