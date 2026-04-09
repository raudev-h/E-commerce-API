from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import Annotated


class ProductCreate(BaseModel):
    name:str = Field(min_length=3)
    description:Annotated[str | None, Field(min_length=10)] = None
    price:float = Field(ge=0)
    stock:int = Field(ge=0)
    category_id:UUID
    image_url:str | None = None

class ProductUpdate(BaseModel):
    name:Annotated[str | None, Field(min_length=3)] = None
    description:Annotated[str | None, Field(min_length=10)] = None
    price:Annotated[float | None, Field(ge=0)] = None
    stock:Annotated[int | None, Field(ge=0)] = None
    category_id:UUID | None = None
    image_url:str | None = None

class ProductResponse(BaseModel):
    id:UUID
    name:str
    description:str | None = None
    price:float
    stock:int
    category_id:UUID
    image_url:str | None = None
    is_active:bool
    created_at:datetime
    updated_at:datetime

    model_config = {"from_attributes": True}