from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session
from utils.password_policy import PasswordPolicy
from pydantic import BaseModel  

from services.user_service import user_service
from database.session import get_db_session
from models.user_models import UserCreate, UserResponse, UserLogin

router = APIRouter()

class PasswordValidationRequest(BaseModel):
    password: str
    
@router.get("/health")
async def health_check(session: Session = Depends(get_db_session)):
    """Health check endpoint"""
    try:
        from sqlmodel import text 
        session.exec(text("SELECT 1")) 
        return {"status": "healthy", "service": "user-service", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "service": "user-service", "database": "disconnected", "error": str(e)}

@router.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate, session: Session = Depends(get_db_session)):
    """Create a new user"""
    return user_service.create_user(user_data, session)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, session: Session = Depends(get_db_session)):
    """Get user by ID"""
    return user_service.get_user_by_id(user_id, session)

@router.get("/email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, session: Session = Depends(get_db_session)):
    """Get user by email"""
    return user_service.get_user_by_email(email, session)

@router.get("/", response_model=List[UserResponse])
async def list_users(session: Session = Depends(get_db_session)):
    """List all users"""
    return user_service.get_all_users(session)

@router.post("/verify-login")
async def verify_login(credentials: UserLogin, session: Session = Depends(get_db_session)):
    """Verify user login credentials"""
    return user_service.verify_login(credentials, session)

@router.get("/debug/user/{email}")
async def debug_user(email: str, session: Session = Depends(get_db_session)):
    """Debug endpoint to see actual stored data"""
    from database.user_repository import UserRepository
    
    repository = UserRepository(session)
    user = repository.get_user_by_email(email)
    if not user:
        return {"error": "User not found"}
    
    return {
        "id": user.user_id,
        "email": user.email,
        "full_name": user.full_name,
        "password_stored": user.password_hash,
        "password_is_hashed": user.password_hash.startswith("$2b$"),
        "created_at": user.created_at.isoformat(),
        "is_active": user.is_active
    }
    
@router.get("/password-policy")
async def get_password_policy():
    """Get enterprise password policy requirements"""
    return PasswordPolicy.get_requirements()

@router.post("/validate-password")
async def validate_password(request: PasswordValidationRequest):
    """Validate password against enterprise security policy"""
    is_valid, errors = PasswordPolicy.validate(request.password)
    
    return {
        "is_valid": is_valid,
        "errors": errors if not is_valid else {},
        "policy": PasswordPolicy.get_requirements()
    }