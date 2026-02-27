from sqlalchemy import func, String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from datetime import datetime
from uuid import UUID, uuid4
import enum

class UserRole(enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    email:Mapped[str] = mapped_column(String(225))

    password:Mapped[str] = mapped_column(String(225))

    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user)

    first_name:Mapped[str] = mapped_column(String(225))

    last_name:Mapped[str] = mapped_column(String(225))

    is_active:Mapped[bool] = mapped_column(Boolean,default=True)

    created_at:Mapped[datetime] = mapped_column(server_default=func.now())

    updated_at:Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())