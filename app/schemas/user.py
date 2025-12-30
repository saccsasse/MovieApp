from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.core.enums import UserRole

class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="User email")
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6, description="User password")
    role: Optional[UserRole] = UserRole.USER

class UserOut(BaseModel):
    id: int = Field(..., description="User unique ID")
    username: str = Field(..., min_length=1, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="User email")
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    role: Optional[UserRole] = UserRole.USER
    is_active: bool = Field(..., description="Is User Active or not")

    model_config = {
        "from_attributes": True
    }

class UserPublic(BaseModel):
    id: int = Field(..., description="User unique ID")
    username: str = Field(..., min_length=1, max_length=50, description="Unique username")
    role: Optional[UserRole] = UserRole.USER

    #allowing conversion from objects (like ORM instances) into the schema.
    model_config = {
        "from_attributes": True
    }