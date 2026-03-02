from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from datetime import datetime
from uuid import UUID, uuid4


class Cart(Base):

    __tablename__ = "cart"

    id:Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    created_at:Mapped[datetime] = mapped_column(server_default=func.now())

    updated_at:Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())