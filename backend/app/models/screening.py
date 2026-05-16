"""Vetítés modell a Mozi Jegyfoglaló rendszerhez."""
from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Screening(Base):
    """Vetítés modell, amely egy film vetítését képviseli.
    
    Attributes:
        id: Elsődleges kulcs
        movie_id: Idegen kulcs a Movie táblára
        screen_number: Vetítőterem száma
        screening_datetime: A vetítés dátuma és ideje
        available_seats: Elérhető székek száma
        total_seats: A terem teljes kapacitása
        price_per_ticket: Jegy ára pénzegységben
        created_at: Rekord létrehozási időbélyeg
        updated_at: Utolsó frissítés időbélyege
        movie: Kapcsolat a Movie modellel
        bookings: Kapcsolat a Booking modellel
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
    
    # Kapcsolatok
    movie = relationship("Movie", back_populates="screenings")
    bookings = relationship("Booking", back_populates="screening", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        """Vetítés szöveges reprezentációja."""
        return f"<Screening(id={self.id}, movie_id={self.movie_id}, seats={self.available_seats}/{self.total_seats})>"
