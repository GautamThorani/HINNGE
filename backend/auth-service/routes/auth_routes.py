from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from services.auth_service import auth_service
from services.user_client import user_client
from middleware.auth_middleware import verify_token
from database.session import get_db_session
from models.auth_models import UserLogin, AuthResponse, TokenVerification, UserRegistration, TokenData

router = APIRouter()

@router.get("/health")
async def health_check(session: Session = Depends(get_db_session)):
    """Health check endpoint"""
    try:
        from sqlmodel import text
        session.exec(text("SELECT 1"))
        return {"status": "healthy", "service": "auth-service", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "service": "auth-service", "database": "disconnected", "error": str(e)}

@router.post("/login", response_model=AuthResponse)
async def login(credentials: UserLogin, session: Session = Depends(get_db_session)):
    """
    Authenticate user and return JWT token
    """
    return await auth_service.login(credentials, session)

@router.post("/register")
async def register(user_data: UserRegistration, session: Session = Depends(get_db_session)):
    """
    Register a new user
    """
    return await auth_service.register(user_data.dict(), session)

@router.get("/validate", response_model=TokenVerification)
async def validate_token(token_data: TokenData = Depends(verify_token)):
    """
    Validate JWT token
    """
    return TokenVerification(
        valid=True,
        user=token_data
    )

@router.get("/me")
async def get_current_user(token_data: TokenData = Depends(verify_token), session: Session = Depends(get_db_session)):
    """
    Get current user information
    """
    try:
        user = await user_client.get_user_by_email(token_data.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    except Exception as e:
        print(f"Error in /me endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch user data")

@router.get("/hash-password/{password}")
async def hash_password_endpoint(password: str):
    """
    Utility endpoint to generate hashed passwords (for testing)
    """
    return {"hashed_password": auth_service.hash_password(password)}