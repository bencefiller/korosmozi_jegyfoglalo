"""Booking schemas for request/response validation."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal


class BookingCreate(BaseModel):
    """Schema for creating a booking."""
    
    screening_id: int = Field(..., gt=0, description="Screening ID")
    seat_number: int = Field(..., ge=1, le=500, description="Seat number (1-500)")


class BookingResponse(BaseModel):
    """Schema for booking response."""
    
    id: int
    user_id: int
    screening_id: int
    seat_number: int
    booking_datetime: datetime
    status: str
    created_at: datetime
    
    class Config:
        """Pydantic config."""
        from_attributes = True


class BookingListResponse(BaseModel):
    """Schema for list of bookings."""
    
    bookings: list[BookingResponse]
    total: int


class BookingDetailResponse(BookingResponse):
    """Extended booking response with screening and movie details."""
    
    movie_title: Optional[str] = None
    screening_datetime: Optional[datetime] = None
    price_per_ticket: Optional[Decimal] = None
