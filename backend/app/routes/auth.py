"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_database
from app.models.user import User
from app.models.session import Session as SessionModel
from app.schemas.user import UserRegister, UserLogin, UserResponse
from app.utils.password import hash_password, verify_password
from app.utils.session import generate_session_id, get_session_expiry
from app.utils.deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=dict, status_code=201)
async def register(
    user_data: UserRegister,
    database: Session = Depends(get_database)
) -> dict:
    """Register a new user.
    
    Args:
        user_data: User registration data
        database: Database session
        
    Returns:
        Dictionary with success message and user data
        
    Raises:
        HTTPException: 400 if user exists, 422 if validation fails
    """
    # Check if user already exists
    existing_user = database.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name
    )
    
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    
    return {
        "success": True,
        "message": "User registered successfully.",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name
        }
    }


@router.post("/login", response_model=dict, status_code=200)
async def login(
    user_data: UserLogin,
    response: Response,
    database: Session = Depends(get_database)
) -> dict:
    """Login user and set session cookie.
    
    Args:
        user_data: User login credentials
        response: FastAPI response object
        database: Database session
        
    Returns:
        Dictionary with success message and user data
        
    Raises:
        HTTPException: 401 if credentials invalid
    """
    # Find user by email
    user = database.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )
    
    # Verify password
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )
    
    # Create session
    session_id = generate_session_id()
    session_record = SessionModel(
        session_id=session_id,
        user_id=user.id,
        expires_at=get_session_expiry()
    )
    
    database.add(session_record)
    database.commit()
    
    # Set session cookie
    response.set_cookie(
        key="session_id",
        value=session_id,
        max_age=86400,  # 24 hours
        httponly=True,
        samesite="lax"
    )
    
    return {
        "success": True,
        "message": "Login successful.",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }


@router.post("/logout", response_model=dict, status_code=200)
async def logout(
    current_user: User = Depends(get_current_user),
    response: Response = None,
    database: Session = Depends(get_database)
) -> dict:
    """Logout user and invalidate session.
    
    Args:
        current_user: Authenticated user
        response: FastAPI response object
        database: Database session
        
    Returns:
        Dictionary with success message
    """
    # Clear session cookie
    if response:
        response.delete_cookie("session_id")
    
    return {
        "success": True,
        "message": "Logout successful."
    }


@router.get("/me", response_model=dict, status_code=200)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> dict:
    """Get current authenticated user information.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Dictionary with user data
    """
    return {
        "success": True,
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "created_at": current_user.created_at.isoformat()
        }
    }
