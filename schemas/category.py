from pydantic import BaseModel, Field
from uuid import UUID
from typing import Annotated

class CategoryCreate(BaseModel):
    name:str = Field(min_length=3)
    description: Annotated[str | None, Field(min_length=10)] = None

class CategoryUpdate(BaseModel):
    name:Annotated[str | None, Field(min_length=3)] = None  
    description: Annotated[str | None, Field(min_length=10)] = None

class CategoryResponse(BaseModel):
    id:UUID
    name:str
    description:str | None = None
    is_active:bool
    model_config = {"from_attributes":True}

