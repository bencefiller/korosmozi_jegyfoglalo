"""Session modell a felhasználói web sessionök kezeléséhez."""
from sqlalchemy import Column, String, Integer, JSON, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Session(Base):
    """Session modell a felhasználói webes sessionök kezeléséhez.
    
    Attributes:
        session_id: Elsődleges kulcs, egyedi session azonosító
        user_id: Idegen kulcs a User táblára (nullable anonim sessionök esetén)
        session_data: JSON adatok a session állapotához
        expires_at: Session lejárati időbélyege
        created_at: Session létrehozási időbélyege
        user: Kapcsolat a User modellel
    """
    
    __tablename__ = "sessions"
    
    session_id = Column(String(255), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    session_data = Column(JSON, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Kapcsolatok
    user = relationship("User", back_populates="sessions")

    def __repr__(self) -> str:
        """String representation of Session."""
        return f"<Session(session_id={self.session_id}, user_id={self.user_id})>"
