from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from .product import ProductResponse


class CartItemAdd(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)


class CartItemUpdateQty(BaseModel):
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    id: UUID
    cart_id: UUID
    product_id: UUID
    quantity: int
    updated_at: datetime
    product: ProductResponse | None = None

    model_config = {"from_attributes": True}


class CartResponse(BaseModel):
    id: UUID
    items: list[CartItemResponse]

    model_config = {"from_attributes": True}
