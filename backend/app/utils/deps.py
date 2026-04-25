"""Dependency injection functions for FastAPI."""
from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_database
from app.models.user import User
from app.models.session import Session as SessionModel


async def get_current_user(
    session_id: Optional[str] = Cookie(None),
    database: Session = Depends(get_database)
) -> User:
    """Get current authenticated user from session cookie.
    
    Args:
        session_id: Session ID from cookie
        database: Database session
        
    Returns:
        User object if authenticated
        
    Raises:
        HTTPException: 401 if not authenticated
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please login first."
        )
    
    # Fetch session from database
    session_record = database.query(SessionModel).filter(
        SessionModel.session_id == session_id,
        SessionModel.expires_at > datetime.utcnow()
    ).first()
    
    if not session_record or not session_record.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session."
        )
    
    # Fetch user
    user = database.query(User).filter(User.id == session_record.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found."
        )
    
    return user


async def get_optional_user(
    session_id: Optional[str] = Cookie(None),
    database: Session = Depends(get_database)
) -> Optional[User]:
    """Get current user if authenticated, otherwise None.
    
    Args:
        session_id: Session ID from cookie
        database: Database session
        
    Returns:
        User object if authenticated, None otherwise
    """
    if not session_id:
        return None
    
    session_record = database.query(SessionModel).filter(
        SessionModel.session_id == session_id,
        SessionModel.expires_at > datetime.utcnow()
    ).first()
    
    if not session_record or not session_record.user_id:
        return None
    
    user = database.query(User).filter(User.id == session_record.user_id).first()
    return user


from datetime import datetime
