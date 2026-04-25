"""Screening routes."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.database import get_database
from app.models.screening import Screening
from app.models.movie import Movie

router = APIRouter(prefix="/api/screenings", tags=["screenings"])


@router.get("", response_model=dict, status_code=200)
async def list_screenings(
    movie_id: Optional[int] = Query(None, description="Filter by movie ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum records to return"),
    database: Session = Depends(get_database)
) -> dict:
    """List screenings with optional movie filter.
    
    Args:
        movie_id: Optional filter by movie ID
        skip: Number of records to skip
        limit: Maximum records to return
        database: Database session
        
    Returns:
        Dictionary with screenings list
    """
    query = database.query(Screening)
    
    # Apply movie filter if provided
    if movie_id:
        query = query.filter(Screening.movie_id == movie_id)
    
    # Get total count
    total = query.count()
    
    # Sort by screening datetime and apply pagination
    screenings = query.order_by(Screening.screening_datetime).offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "data": {
            "screenings": [
                {
                    "id": screening.id,
                    "movie_id": screening.movie_id,
                    "screen_number": screening.screen_number,
                    "screening_datetime": screening.screening_datetime.isoformat(),
                    "available_seats": screening.available_seats,
                    "total_seats": screening.total_seats,
                    "price_per_ticket": float(screening.price_per_ticket)
                }
                for screening in screenings
            ],
            "total": total,
            "skip": skip,
            "limit": limit
        }
    }


@router.get("/{screening_id}", response_model=dict, status_code=200)
async def get_screening(
    screening_id: int,
    database: Session = Depends(get_database)
) -> dict:
    """Get screening details by ID with movie information.
    
    Args:
        screening_id: Screening ID
        database: Database session
        
    Returns:
        Dictionary with screening details and available seats info
        
    Raises:
        HTTPException: 404 if screening not found
    """
    screening = database.query(Screening).filter(Screening.id == screening_id).first()
    
    if not screening:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screening not found."
        )
    
    movie = screening.movie
    
    return {
        "success": True,
        "data": {
            "id": screening.id,
            "movie_id": screening.movie_id,
            "movie": {
                "id": movie.id,
                "title": movie.title,
                "genre": movie.genre,
                "duration_minutes": movie.duration_minutes
            } if movie else None,
            "screen_number": screening.screen_number,
            "screening_datetime": screening.screening_datetime.isoformat(),
            "available_seats": screening.available_seats,
            "total_seats": screening.total_seats,
            "price_per_ticket": float(screening.price_per_ticket)
        }
    }
