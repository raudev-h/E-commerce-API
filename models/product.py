from sqlalchemy import ForeignKey, String, Float, Integer, Boolean, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from uuid import UUID, uuid4
from datetime import datetime

class Product(Base):

    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("price > 0", name="price_positive"),
        CheckConstraint("stock >= 0", name="stock_non_negative")
    )

    id:Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    name:Mapped[str] = mapped_column(String(100))

    description:Mapped[str | None] = mapped_column(String(500), nullable=True)

    price:Mapped[float] = mapped_column(Float)

    stock:Mapped[int] = mapped_column(Integer)

    category_id:Mapped[UUID] = mapped_column(ForeignKey("category.id"))

    is_active:Mapped[bool] = mapped_column(Boolean, default=True)

    created_at:Mapped[datetime] = mapped_column(server_default=func.now())

    updated_at:Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

