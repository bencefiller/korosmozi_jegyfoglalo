"""FastAPI-függőséginjektálási segédfüggvények."""
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
    """A jelenlegi hitelesített felhasználó lekérése a session sütiből.
    
    Args:
        session_id: A süti alapján kapott session azonosító
        database: Adatbázis-session
        
    Returns:
        Felhasználó objektum, ha hitelesített
        
    Raises:
        HTTPException: 401 ha nincs hitelesítve
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nem vagy hitelesítve. Kérlek jelentkezz be előbb."
        )
    
    # Session lekérése az adatbázisból
    session_record = database.query(SessionModel).filter(
        SessionModel.session_id == session_id,
        SessionModel.expires_at > datetime.utcnow()
    ).first()
    
    if not session_record or not session_record.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Érvénytelen vagy lejárt session."
        )
    
    # Felhasználó lekérése
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
    """Lekéri a jelenlegi felhasználót, ha hitelesített, egyébként None-t ad.
    
    Args:
        session_id: A süti alapján kapott session azonosító
        database: Adatbázis-session
        
    Returns:
        Felhasználó objektum, ha hitelesített, egyébként None
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
