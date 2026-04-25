"""Booking model for Cinema Booking System."""
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, func, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base


class BookingStatus(PyEnum):
    """Enum for booking status."""
    ACTIVE = "active"
    CANCELLED = "cancelled"


class Booking(Base):
    """Booking model representing a ticket reservation.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to User
        screening_id: Foreign key to Screening
        seat_number: Seat number (1-100)
        booking_datetime: When the booking was made
        status: Booking status (active or cancelled)
        created_at: Record creation timestamp
        updated_at: Last update timestamp
        user: Relationship to User model
        screening: Relationship to Screening model
    """
    
    __tablename__ = "bookings"
    __table_args__ = (
        UniqueConstraint("screening_id", "seat_number", name="uq_screening_seat"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    screening_id = Column(Integer, ForeignKey("screenings.id", ondelete="CASCADE"), nullable=False, index=True)
    seat_number = Column(Integer, nullable=False)
    booking_datetime = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default=BookingStatus.ACTIVE.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    screening = relationship("Screening", back_populates="bookings")
    
    def __repr__(self) -> str:
        """String representation of Booking."""
        return f"<Booking(id={self.id}, user_id={self.user_id}, screening_id={self.screening_id}, seat={self.seat_number})>"
