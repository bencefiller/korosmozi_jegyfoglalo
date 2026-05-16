"""Hitelesítési útvonalak."""
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie, Header
from sqlalchemy.orm import Session as DBSession
from typing import Optional
from pydantic import BaseModel
import uuid
import bcrypt
from datetime import datetime, timedelta, timezone

from app.database import get_database
from app.models.user import User
from app.models.session import Session as UserSession

router = APIRouter(prefix="/api/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str

class LoginRequest(BaseModel):
    email: str
    password: str

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

@router.post("/register", status_code=201)
async def register(request: RegisterRequest, response: Response, db: DBSession = Depends(get_database)):
    # E-mail cím normalizálása (kisbetűsítés és láthatatlan szóközök levágása)
    safe_email = request.email.lower().strip()
    
    if db.query(User).filter(User.email == safe_email).first():
        raise HTTPException(status_code=400, detail="Ez az email cím már regisztrálva van.")
    
    new_user = User(
        email=safe_email,
        password_hash=get_password_hash(request.password),
        full_name=request.full_name
    )

    db.add(new_user)
    db.commit()
    
    # Automatikus bejelentkezés regisztráció után
    session_id = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    new_session = UserSession(session_id=session_id, user_id=new_user.id, expires_at=expires_at)
    db.add(new_session)
    db.commit()
    
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=86400, samesite="lax", secure=False)
    
    return {"success": True, "message": "Sikeres regisztráció.", "session_id": session_id, "user": {"id": new_user.id, "email": new_user.email, "full_name": new_user.full_name}}

@router.post("/login")
async def login(request: LoginRequest, response: Response, db: DBSession = Depends(get_database)):
    # Ugyanúgy normalizáljuk a bejelentkezésnél is az e-mailt
    safe_email = request.email.lower().strip()
    user = db.query(User).filter(User.email == safe_email).first()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Hibás email vagy jelszó.")

    
    session_id = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    
    new_session = UserSession(session_id=session_id, user_id=user.id, expires_at=expires_at)
    db.add(new_session)
    db.commit()
    
    # Sütik beállítása a Frontend számára
    response.set_cookie(
        key="session_id", 
        value=session_id, 
        httponly=True, 
        max_age=86400, 
        samesite="lax",
        secure=False
    )
    
    return {"success": True, "message": "Sikeres bejelentkezés.", "session_id": session_id, "user": {"id": user.id, "email": user.email, "full_name": user.full_name}}

@router.get("/me")
async def get_me(session_id: Optional[str] = Cookie(None), x_session_id: Optional[str] = Header(None), db: DBSession = Depends(get_database)):
    actual_session = x_session_id or session_id
    if not actual_session:
        raise HTTPException(status_code=401, detail="Nincs bejelentkezve.")
        
    session = db.query(UserSession).filter(UserSession.session_id == actual_session).first()
    if not session or session.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session lejárt.")
        
    user = db.query(User).filter(User.id == session.user_id).first()
    return {"success": True, "user": {"id": user.id, "email": user.email, "full_name": user.full_name}}

@router.post("/logout")
async def logout(response: Response, session_id: Optional[str] = Cookie(None), x_session_id: Optional[str] = Header(None), db: DBSession = Depends(get_database)):
    actual_session = x_session_id or session_id
    if actual_session:
        session = db.query(UserSession).filter(UserSession.session_id == actual_session).first()
        if session:
            db.delete(session)
            db.commit()
            
    response.delete_cookie("session_id")
    return {"success": True, "message": "Sikeres kijelentkezés."}

@router.get("/users")
async def get_all_users(db: DBSession = Depends(get_database)):
    """Fejlesztői végpont: kilistázza az összes regisztrált felhasználót az adatbázisból."""
    users = db.query(User).all()
    return {
        "success": True,
        "users": [
            {"id": u.id, "email": u.email, "full_name": u.full_name} for u in users
        ]
    }