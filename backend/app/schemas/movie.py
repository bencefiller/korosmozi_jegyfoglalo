"""Movie schemas for request/response validation."""
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List


class MovieCreate(BaseModel):
    """Schema for creating a movie."""
    
    title: str = Field(..., min_length=1, max_length=255, description="Movie title")
    description: Optional[str] = Field(None, description="Movie description")
    duration_minutes: int = Field(..., gt=0, description="Duration in minutes")
    genre: Optional[str] = Field(None, max_length=100, description="Movie genre")
    release_date: Optional[date] = Field(None, description="Release date")
    poster_url: Optional[str] = Field(None, max_length=500, description="URL to poster image")


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
