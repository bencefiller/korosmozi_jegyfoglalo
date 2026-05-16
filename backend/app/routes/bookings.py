"""Booking routes."""
from fastapi import APIRouter, Depends, HTTPException, Cookie, Header
from sqlalchemy.orm import Session as DBSession
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel

from app.database import get_database
from app.models.booking import Booking
from app.models.screening import Screening
from app.models.session import Session as UserSession
from app.models.user import User

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

# Belső Pydantic sémák a beérkező adatok validálására
class BookingCreate(BaseModel):
    screening_id: int
    seat_number: int

def get_current_user(session_id: Optional[str] = Cookie(None), x_session_id: Optional[str] = Header(None), db: DBSession = Depends(get_database)):
    """Segédfüggvény, amely a süti alapján visszaadja a bejelentkezett felhasználót."""
    actual_session = x_session_id or session_id
    if not actual_session:
        raise HTTPException(status_code=401, detail="Nincs bejelentkezve.")
        
    session = db.query(UserSession).filter(UserSession.session_id == actual_session).first()
    if not session or session.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session lejárt, jelentkezz be újra.")
        
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Felhasználó nem található.")
    return user

@router.post("", status_code=201)
async def create_booking(
    request: BookingCreate, 
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_database)
):
    screening = db.query(Screening).filter(Screening.id == request.screening_id).first()
    if not screening:
        raise HTTPException(status_code=404, detail="Vetítés nem található.")
        
    if request.seat_number < 1 or request.seat_number > screening.total_seats:
        raise HTTPException(status_code=400, detail="Érvénytelen szék szám.")
        
    # Ellenőrizzük, hogy a szék foglalt-e már
    existing_booking = db.query(Booking).filter(
        Booking.screening_id == request.screening_id,
        Booking.seat_number == request.seat_number,
        Booking.status == "active"
    ).first()
    
    if existing_booking:
        raise HTTPException(status_code=409, detail="Ez a szék már foglalt.")
        
    if screening.available_seats <= 0:
        raise HTTPException(status_code=400, detail="Nincs több szabad hely a vetítésen.")
        
    # Foglalás létrehozása és szabad helyek csökkentése
    new_booking = Booking(
        user_id=user.id,
        screening_id=screening.id,
        seat_number=request.seat_number,
        status="active"
    )
    screening.available_seats -= 1
    
    db.add(new_booking)
    db.commit()
    
    return {"success": True, "data": {"id": new_booking.id}}

@router.get("/screening/{screening_id}")
async def get_booked_seats(screening_id: int, db: DBSession = Depends(get_database)):
    """Visszaadja egy vetítés összes aktív foglalásának székszámait."""
    bookings = db.query(Booking).filter(
        Booking.screening_id == screening_id,
        Booking.status == "active"
    ).all()
    
    booked_seats = [b.seat_number for b in bookings]
    return {"success": True, "data": {"booked_seats": booked_seats}}

@router.get("")
async def get_bookings(user: User = Depends(get_current_user), db: DBSession = Depends(get_database)):
    """Lekéri a bejelentkezett felhasználó összes foglalását."""
    bookings = db.query(Booking).filter(Booking.user_id == user.id).order_by(Booking.created_at.desc()).all()
    
    result = []
    for b in bookings:
        screening = db.query(Screening).filter(Screening.id == b.screening_id).first()
        movie_title = screening.movie.title if screening and screening.movie else "Ismeretlen film"
        poster_url = screening.movie.poster_url if screening and screening.movie else None
        screening_time = screening.screening_datetime if screening else datetime.now()
        price = screening.price_per_ticket if screening else 0
        
        result.append({
            "id": b.id,
            "screening_id": b.screening_id,
            "seat_number": b.seat_number,
            "status": b.status,
            "movie_title": movie_title,
            "poster_url": poster_url,
            "screening_datetime": screening_time.isoformat() if hasattr(screening_time, 'isoformat') else str(screening_time),
            "price": float(price)
        })
        
    return {"success": True, "data": {"bookings": result}}

@router.delete("/{booking_id}")
async def cancel_booking(booking_id: int, user: User = Depends(get_current_user), db: DBSession = Depends(get_database)):
    """Foglalás lemondása."""
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Foglalás nem található.")
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="A foglalás már le van mondva.")
        
    booking.status = "cancelled"
    screening = db.query(Screening).filter(Screening.id == booking.screening_id).first()
    if screening:
        screening.available_seats += 1
        
    db.commit()
    return {"success": True, "message": "Foglalás sikeresen lemondva."}