from pydantic import BaseModel
from uuid import UUID
from .product import ProductResponse


class OrderItemResponse(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: float
    product: ProductResponse | None = None

    model_config = {"from_attributes": True}
