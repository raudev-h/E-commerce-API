from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class CartItemAdd(BaseModel):
    user_id:UUID
    product_id:UUID
    quantity:int = Field(gt=0)

class CartItemResponse(BaseModel):
    id:UUID
    cart_id:UUID
    product_id:UUID
    quantity:int
    updated_at:datetime

    model_config={"from_attributes":True}