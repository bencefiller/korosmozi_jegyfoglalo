"""Screening schemas for request/response validation."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class ScreeningCreate(BaseModel):
    """Schema for creating a screening."""
    
    movie_id: int = Field(..., gt=0, description="Movie ID")
    screen_number: int = Field(..., gt=0, description="Screen number")
    screening_datetime: datetime = Field(..., description="Screening date and time")
    available_seats: int = Field(..., gt=0, description="Number of available seats")
    total_seats: int = Field(100, gt=0, description="Total seat capacity")
    price_per_ticket: Decimal = Field(..., gt=0, decimal_places=2, description="Price per ticket")


class ScreeningResponse(BaseModel):
    """Schema for screening response."""
    
    id: int
    movie_id: int
    screen_number: int
    screening_datetime: datetime
    available_seats: int
    total_seats: int
    price_per_ticket: Decimal
    created_at: datetime
    
    class Config:
        """Pydantic config."""
        from_attributes = True


class ScreeningDetailResponse(ScreeningResponse):
    """Extended screening response with movie details."""
    
    movie: Optional[dict] = None
