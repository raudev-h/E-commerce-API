from pydantic import BaseModel
from uuid import UUID


class OrderItemResponse(BaseModel):
    id:UUID
    order_id:UUID
    product_id:UUID
    quantity:int
    unit_price:float