from pydantic import BaseModel
from models.order import Status
from uuid import UUID
from datetime import datetime



class OrderResponse(BaseModel):
    id:UUID
    user_id:UUID
    status:Status
    total:float
    created_at:datetime
    updated_at:datetime

    model_config = {"from_attributes":True}