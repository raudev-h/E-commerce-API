from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from uuid import UUID
from datetime import datetime
from typing import Annotated
from models.user import UserRole

class UserCreate(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    email:EmailStr
    password:str
    confirm_password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("password most have 8 characters")
        return value
    
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("passwords do not match")
        return self
    
    @field_validator("email")
    @classmethod
    def normalize_email(cls, value:str):
        return value.lower()
    
class UserUpdateProfile(BaseModel):
    first_name:Annotated[str | None, Field(min_length=2)] = None
    last_name:Annotated[str | None, Field(min_length=2)] = None

class UserAdminUpdate(BaseModel):
    first_name:Annotated[str | None, Field(min_length=2)] = None
    last_name:Annotated[str | None, Field(min_length=2)] = None
    role: UserRole | None = None
    is_active: bool | None = None

class UserResponse(BaseModel):
    id:UUID
    first_name:str
    last_name:str
    email:EmailStr
    role:UserRole
    is_active:bool
    created_at:datetime
    updated_at:datetime

    model_config = {"from_attributes": True}