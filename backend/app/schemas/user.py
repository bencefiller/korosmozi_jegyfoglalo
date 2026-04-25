"""User schemas for request/response validation."""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserRegister(BaseModel):
    """Schema for user registration."""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=255, description="Password (minimum 8 characters)")
    full_name: str = Field(..., min_length=2, max_length=255, description="User's full name")


class UserLogin(BaseModel):
    """Schema for user login."""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserResponse(BaseModel):
    """Schema for user response (without password)."""
    
    id: int
    email: str
    full_name: str
    created_at: datetime
    
    class Config:
        """Pydantic config."""
        from_attributes = True
