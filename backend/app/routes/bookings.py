"""Booking routes - CORE BUSINESS LOGIC."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_database
from app.models.booking import Booking
from app.models.screening import Screening
from app.models.user import User
from app.schemas.booking import BookingCreate
from app.utils.deps import get_current_user

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.post("", response_model=dict, status_code=201)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    database: Session = Depends(get_database)
) -> dict:
    """Create a new booking (ticket reservation).
    
    CRITICAL BUSINESS LOGIC:
    1. Validate screening exists and seat number is valid (1-100)
    2. Check if seat is already booked (UNIQUE constraint)
    3. Verify available seats count is > 0
    4. Decrement available_seats
    5. Create booking record
    6. Commit atomically (all or nothing)
    
    Args:
        booking_data: Booking creation data (screening_id, seat_number)
        current_user: Authenticated user
        database: Database session
        
    Returns:
        Dictionary with created booking details
        
    Raises:
        HTTPException: 400 if validation fails, 404 if screening not found,
                      409 if seat already booked
    """
    # Validate seat number
    if booking_data.seat_number < 1 or booking_data.seat_number > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seat number must be between 1 and 100."
        )
    
    # Fetch screening
    screening = database.query(Screening).filter(
        Screening.id == booking_data.screening_id
    ).first()
    
    if not screening:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screening not found."
        )
    
    # Check available seats
    if screening.available_seats <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No available seats for this screening."
        )
    
    try:
        # Create booking (UNIQUE constraint will catch duplicate seats)
        new_booking = Booking(
            user_id=current_user.id,
            screening_id=booking_data.screening_id,
            seat_number=booking_data.seat_number,
            status="active"
        )
        
        database.add(new_booking)
        
        # Decrement available seats atomically
        screening.available_seats -= 1
        database.add(screening)
        
        # Commit atomically
        database.commit()
        database.refresh(new_booking)
        
        return {
            "success": True,
            "message": "Booking created successfully.",
            "data": {
                "id": new_booking.id,
                "user_id": new_booking.user_id,
                "screening_id": new_booking.screening_id,
                "seat_number": new_booking.seat_number,
                "status": new_booking.status,
                "booking_datetime": new_booking.booking_datetime.isoformat(),
                "price": float(screening.price_per_ticket)
            }
        }
    
    except IntegrityError:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat already booked for this screening."
        )


@router.get("", response_model=dict, status_code=200)
async def list_user_bookings(
    current_user: User = Depends(get_current_user),
    database: Session = Depends(get_database)
) -> dict:
    """List all bookings for the authenticated user.
    
    Args:
        current_user: Authenticated user
        database: Database session
        
    Returns:
        Dictionary with user's bookings
    """
    bookings = database.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.status == "active"
    ).all()
    
    return {
        "success": True,
        "data": {
            "bookings": [
                {
                    "id": booking.id,
                    "screening_id": booking.screening_id,
                    "seat_number": booking.seat_number,
                    "status": booking.status,
                    "booking_datetime": booking.booking_datetime.isoformat(),
                    "movie_title": booking.screening.movie.title if booking.screening.movie else None,
                    "screening_datetime": booking.screening.screening_datetime.isoformat(),
                    "price": float(booking.screening.price_per_ticket)
                }
                for booking in bookings
            ],
            "total": len(bookings)
        }
    }


@router.delete("/{booking_id}", response_model=dict, status_code=200)
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    database: Session = Depends(get_database)
) -> dict:
    """Cancel a booking (refund and free up seat).
    
    Args:
        booking_id: Booking ID to cancel
        current_user: Authenticated user (must own the booking)
        database: Database session
        
    Returns:
        Dictionary with cancellation confirmation
        
    Raises:
        HTTPException: 403 if user doesn't own booking, 404 if booking not found
    """
    booking = database.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found."
        )
    
    # Verify ownership
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel your own bookings."
        )
    
    # Update booking status
    booking.status = "cancelled"
    
    # Free up seat
    screening = booking.screening
    screening.available_seats += 1
    
    database.add(booking)
    database.add(screening)
    database.commit()
    
    return {
        "success": True,
        "message": "Booking cancelled successfully.",
        "data": {
            "id": booking.id,
            "status": booking.status
        }
    }


@router.get("/{booking_id}", response_model=dict, status_code=200)
async def get_booking_details(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    database: Session = Depends(get_database)
) -> dict:
    """Get booking details (authenticated user only).
    
    Args:
        booking_id: Booking ID
        current_user: Authenticated user
        database: Database session
        
    Returns:
        Dictionary with booking details
        
    Raises:
        HTTPException: 403 if user doesn't own booking, 404 if booking not found
    """
    booking = database.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found."
        )
    
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own bookings."
        )
    
    return {
        "success": True,
        "data": {
            "id": booking.id,
            "user_id": booking.user_id,
            "screening_id": booking.screening_id,
            "seat_number": booking.seat_number,
            "status": booking.status,
            "booking_datetime": booking.booking_datetime.isoformat(),
            "movie_title": booking.screening.movie.title if booking.screening.movie else None,
            "screening_datetime": booking.screening.screening_datetime.isoformat(),
            "price": float(booking.screening.price_per_ticket)
        }
    }
