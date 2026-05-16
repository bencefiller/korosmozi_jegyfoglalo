"""Felhasználó sémák kérés/válasz validáláshoz."""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserRegister(BaseModel):
    """Felhasználó regisztrációs séma."""
    
    email: EmailStr = Field(..., description="Felhasználó email címe")
    password: str = Field(..., min_length=8, max_length=255, description="Jelszó (minimum 8 karakter)")
    full_name: str = Field(..., min_length=2, max_length=255, description="Felhasználó teljes neve")


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
