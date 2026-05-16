"""Felhasználó modell a Mozi Jegyfoglaló rendszerhez."""
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    """Felhasználó modell, amely egy mozi ügyfelet képvisel.
    
    Attributes:
        id: Elsődleges kulcs
        email: Felhasználó email címe (egyedi)
        password_hash: Bcrypt-tel hash-elt jelszó
        full_name: Felhasználó teljes neve
        created_at: Fiók létrehozásának időbélyege
        updated_at: Utolsó frissítés időbélyege
        bookings: Kapcsolat a Booking modellel
        sessions: Kapcsolat a Session modellel
    """
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Kapcsolatok
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        """Felhasználó szöveges reprezentációja."""
        return f"<User(id={self.id}, email={self.email}, full_name={self.full_name})>"
