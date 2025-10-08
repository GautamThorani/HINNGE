from fastapi import HTTPException
from typing import List
from sqlmodel import Session
from utils.password_policy import PasswordPolicy

from database.user_repository import UserRepository
from models.user_models import UserCreate, UserResponse, UserLogin

class UserService:
    """User service handling business logic with database"""
    
    @staticmethod
    def create_user(user_data: UserCreate, session: Session) -> UserResponse:
        """Create a new user with password validation"""
        try:
            is_valid, errors = PasswordPolicy.validate(user_data.password)
            if not is_valid:
                error_message = "Password does not meet security requirements: "
                error_message += "; ".join(errors.values())
                raise ValueError(error_message)
            
            repository = UserRepository(session)
            user = repository.create_user(user_data)
            return UserService._to_user_response(user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @staticmethod
    def get_user_by_id(user_id: str, session: Session) -> UserResponse:
        """Get user by ID"""
        repository = UserRepository(session)
        user = repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserService._to_user_response(user)
    
    @staticmethod
    def get_user_by_email(email: str, session: Session) -> UserResponse:
        """Get user by email"""
        repository = UserRepository(session)
        user = repository.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserService._to_user_response(user)
    
    @staticmethod
    def get_all_users(session: Session) -> List[UserResponse]:
        """Get all users"""
        repository = UserRepository(session)
        users = repository.get_all_users()
        return [UserService._to_user_response(user) for user in users]
    
    @staticmethod
    def verify_login(credentials: UserLogin, session: Session) -> dict:
        """Verify user login credentials"""
        repository = UserRepository(session)
        user = repository.verify_credentials(credentials.email, credentials.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        return {
            "success": True,
            "user_id": user.user_id,
            "email": user.email
        }
    
    @staticmethod
    def _to_user_response(user) -> UserResponse:
        """Convert database user to response model"""
        return UserResponse(
            id=user.user_id, 
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at.isoformat(),
            is_active=user.is_active
        )

user_service = UserService()