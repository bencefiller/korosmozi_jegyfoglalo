"""Movie model for Cinema Booking System."""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Movie(Base):
    """Movie model representing a cinema film.
    
    Attributes:
        id: Primary key
        title: Movie title
        description: Movie description
        duration_minutes: Duration in minutes
        genre: Movie genre
        release_date: Original release date
        poster_url: URL to movie poster image
        created_at: Record creation timestamp
        updated_at: Last update timestamp
        screenings: Relationship to Screening model
    """
    
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    genre = Column(String(100), nullable=True)
    release_date = Column(Date, nullable=True)
    poster_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    screenings = relationship("Screening", back_populates="movie", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        """String representation of Movie."""
        return f"<Movie(id={self.id}, title={self.title}, duration={self.duration_minutes}min)>"
