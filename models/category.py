from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from uuid import uuid4, UUID

class Category(Base):

    __tablename__ = "category"

    id:Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    name:Mapped[str] = mapped_column(String(120), unique=True)

    description:Mapped[str | None] = mapped_column(String(300), nullable=True)

    is_active:Mapped[bool] = mapped_column(Boolean, default=True)
