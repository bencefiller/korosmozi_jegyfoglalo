"""Vetítési útvonalak."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_database
from app.models.screening import Screening

router = APIRouter(prefix="/api/screenings", tags=["screenings"])

@router.get("", response_model=dict, status_code=200)
async def list_screenings(
    movie_id: Optional[int] = Query(None, description="Szűrés film azonosítója szerint"),
    database: Session = Depends(get_database)
) -> dict:
    """Vetítések listázása."""
    query = database.query(Screening)
    
    # Ha a frontend egy specifikus filmet keres (pl. /api/screenings?movie_id=1)
    if movie_id:
        query = query.filter(Screening.movie_id == movie_id)
        
    screenings = query.all()
    
    return {
        "success": True,
        "data": {
            "screenings": [
                {
                    "id": s.id,
                    "movie_id": s.movie_id,
                    "screen_number": s.screen_number,
                    "screening_datetime": s.screening_datetime.isoformat(),
                    "available_seats": s.available_seats,
                    "total_seats": s.total_seats,
                    "price_per_ticket": float(s.price_per_ticket)
                }
                for s in screenings
            ]
        }
    }