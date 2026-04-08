from pydantic import BaseModel
from models.order import Status
from uuid import UUID
from datetime import datetime
from .order_item import OrderItemResponse


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: Status
    total: float
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse] = []

    model_config = {"from_attributes": True}
