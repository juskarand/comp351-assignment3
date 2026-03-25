from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=200)

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=200)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

class ItemResponse(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str]
    quantity: int
    unit_price: float
    reorder_level: int
    location: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True
