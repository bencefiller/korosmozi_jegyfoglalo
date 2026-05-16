"""Film sémák kérés/válasz validáláshoz."""
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List


class MovieCreate(BaseModel):
    """Film létrehozásához használt séma."""
    
    title: str = Field(..., min_length=1, max_length=255, description="Film címe")
    description: Optional[str] = Field(None, description="Film leírása")
    duration_minutes: int = Field(..., gt=0, description="Hossz percekben")
    genre: Optional[str] = Field(None, max_length=100, description="Film műfaja")
    release_date: Optional[date] = Field(None, description="Megjelenési dátum")
    poster_url: Optional[str] = Field(None, max_length=500, description="Plakát kép URL-je")


class MovieResponse(BaseModel):
    """Schema for movie response."""
    
    id: int
    title: str
    description: Optional[str]
    duration_minutes: int
    genre: Optional[str]
    release_date: Optional[date]
    poster_url: Optional[str]
    created_at: datetime
    
    class Config:
        """Pydantic config."""
        from_attributes = True


class MovieListResponse(BaseModel):
    """Schema for list of movies."""
    
    movies: List[MovieResponse]
    total: int
    page: int
    page_size: int
