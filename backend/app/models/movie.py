"""Film modell a Mozi Jegyfoglaló rendszerhez."""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Movie(Base):
    """Film modell, amely egy mozi filmet képvisel.
    
    Attributes:
        id: Elsődleges kulcs
        title: Film címe
        description: Film leírása
        duration_minutes: Hossz percekben
        genre: Film műfaja
        release_date: Eredeti megjelenési dátum
        poster_url: Film plakát URL-je
        created_at: Rekord létrehozási időbélyeg
        updated_at: Utolsó frissítés időbélyege
        screenings: Kapcsolat a Screening modellel
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
    
    # Kapcsolatok
    screenings = relationship("Screening", back_populates="movie", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        """Film szöveges reprezentációja."""
        return f"<Movie(id={self.id}, title={self.title}, duration={self.duration_minutes}min)>"
