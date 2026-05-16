"""Foglalás modell a Mozi Jegyfoglaló rendszerhez."""
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, func, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base


class BookingStatus(PyEnum):
    """Enum a foglalás státuszához."""
    ACTIVE = "active"
    CANCELLED = "cancelled"


class Booking(Base):
    """Foglalás modell, amely egy jegyfoglalást képvisel.
    
    Attributes:
        id: Elsődleges kulcs
        user_id: Idegen kulcs a User táblára
        screening_id: Idegen kulcs a Screening táblára
        seat_number: Szék száma (1-100)
        booking_datetime: Mikor készült a foglalás
        status: Foglalás státusza (active vagy cancelled)
        created_at: Rekord létrehozási időbélyeg
        updated_at: Utolsó frissítés időbélyege
        user: Kapcsolat a User modellel
        screening: Kapcsolat a Screening modellel
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
    
    # Kapcsolatok
    user = relationship("User", back_populates="bookings")
    screening = relationship("Screening", back_populates="bookings")

    def __repr__(self) -> str:
        """Foglalás szöveges reprezentációja."""
        return f"<Booking(id={self.id}, user_id={self.user_id}, screening_id={self.screening_id}, seat={self.seat_number})>"
