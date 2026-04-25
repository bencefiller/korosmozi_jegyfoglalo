"""Screening model for Cinema Booking System."""
from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Screening(Base):
    """Screening model representing a movie screening session.
    
    Attributes:
        id: Primary key
        movie_id: Foreign key to Movie
        screen_number: Cinema screen number
        screening_datetime: Date and time of screening
        available_seats: Number of available seats
        total_seats: Total capacity of the screen
        price_per_ticket: Price per ticket in currency units
        created_at: Record creation timestamp
        updated_at: Last update timestamp
        movie: Relationship to Movie model
        bookings: Relationship to Booking model
    """
    
    __tablename__ = "screenings"
    __table_args__ = (
        UniqueConstraint("screen_number", "screening_datetime", name="uq_screen_datetime"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    screen_number = Column(Integer, nullable=False)
    screening_datetime = Column(DateTime(timezone=True), nullable=False, index=True)
    available_seats = Column(Integer, nullable=False)
    total_seats = Column(Integer, nullable=False, default=100)
    price_per_ticket = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    movie = relationship("Movie", back_populates="screenings")
    bookings = relationship("Booking", back_populates="screening", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        """String representation of Screening."""
        return f"<Screening(id={self.id}, movie_id={self.movie_id}, seats={self.available_seats}/{self.total_seats})>"
