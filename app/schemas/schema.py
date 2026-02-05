from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email:EmailStr
    name:str


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)
    role: str = "employee"
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password too long (max 72 bytes)")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id:int
    created_at:datetime
    role:str

    class Config:
        from_attributes = True 

class UserUpadte(BaseModel):
    name: Optional[str] = None

    class Config:
        from_attributes = True

class UpdateRoleSchema(BaseModel):
    role:str


class PasswordChange(BaseModel):
    old_password:str
    new_password:str
