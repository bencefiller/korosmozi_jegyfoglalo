"""Vetítés sémák kérés/válasz validáláshoz."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class ScreeningCreate(BaseModel):
    """Vetítés létrehozásához használt séma."""
    
    movie_id: int = Field(..., gt=0, description="Film azonosító")
    screen_number: int = Field(..., gt=0, description="Vetítőterem száma")
    screening_datetime: datetime = Field(..., description="Vetítés időpontja")
    available_seats: int = Field(..., gt=0, description="Elérhető székek száma")
    total_seats: int = Field(100, gt=0, description="Összes ülőhely")
    price_per_ticket: Decimal = Field(..., gt=0, decimal_places=2, description="Jegyár")


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
