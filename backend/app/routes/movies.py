"""Movie routes."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_database
from app.models.movie import Movie
from app.schemas.movie import MovieResponse, MovieListResponse

router = APIRouter(prefix="/api/movies", tags=["movies"])


@router.get("", response_model=dict, status_code=200)
async def list_movies(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum records to return"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    database: Session = Depends(get_database)
) -> dict:
    """List all movies with pagination and optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum records to return
        genre: Optional genre filter
        database: Database session
        
    Returns:
        Dictionary with movies list and pagination info
    """
    query = database.query(Movie)
    
    # Apply genre filter if provided
    if genre:
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    movies = query.offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "data": {
            "movies": [
                {
                    "id": movie.id,
                    "title": movie.title,
                    "description": movie.description,
                    "duration_minutes": movie.duration_minutes,
                    "genre": movie.genre,
                    "release_date": movie.release_date.isoformat() if movie.release_date else None,
                    "poster_url": movie.poster_url
                }
                for movie in movies
            ],
            "total": total,
            "skip": skip,
            "limit": limit
        }
    }


@router.get("/{movie_id}", response_model=dict, status_code=200)
async def get_movie(
    movie_id: int,
    database: Session = Depends(get_database)
) -> dict:
    """Get movie details by ID.
    
    Args:
        movie_id: Movie ID
        database: Database session
        
    Returns:
        Dictionary with movie details and screenings
        
    Raises:
        HTTPException: 404 if movie not found
    """
    movie = database.query(Movie).filter(Movie.id == movie_id).first()
    
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found."
        )
    
    return {
        "success": True,
        "data": {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "duration_minutes": movie.duration_minutes,
            "genre": movie.genre,
            "release_date": movie.release_date.isoformat() if movie.release_date else None,
            "poster_url": movie.poster_url,
            "screenings_count": len(movie.screenings)
        }
    }
