"""Session model for web session management."""
from sqlalchemy import Column, String, Integer, JSON, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Session(Base):
    """Session model for managing user web sessions.
    
    Attributes:
        session_id: Primary key, unique session identifier
        user_id: Foreign key to User (nullable for anonymous sessions)
        session_data: JSON data for session state
        expires_at: Expiration timestamp of session
        created_at: Session creation timestamp
        user: Relationship to User model
    """
    
    __tablename__ = "sessions"
    
    session_id = Column(String(255), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    session_data = Column(JSON, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self) -> str:
        """String representation of Session."""
        return f"<Session(session_id={self.session_id}, user_id={self.user_id})>"
