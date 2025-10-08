from fastapi import HTTPException, status
from passlib.context import CryptContext
import bcrypt as bcrypt_lib
import httpx
from sqlmodel import Session

from services.jwt_service import jwt_service
from services.user_client import user_client
from models.auth_models import UserLogin, AuthResponse, Token

class AuthService:
    """Authentication service handling business logic with database integration"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def login(self, credentials: UserLogin, session: Session) -> AuthResponse:
        """Authenticate user and return JWT token with database audit logging"""
        print(f"Login attempt for: {credentials.email}")
        
        is_valid, user_data = await user_client.verify_user_credentials(
            credentials.email, 
            credentials.password
        )
        
        if not is_valid or not user_data:
            print(f"Invalid credentials for: {credentials.email}")
            
            await self._log_audit_event(
                user_id="unknown",
                event_type="login_failed",
                details=f"Failed login attempt for {credentials.email}",
                ip_address="unknown"
            )
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        print(f"User authenticated: {user_data}")
        
        await self._log_audit_event(
            user_id=user_data["user_id"],
            event_type="login_success",
            details=f"User {credentials.email} logged in successfully",
            ip_address="unknown"
        )
        
        token_data = {
            "user_id": user_data["user_id"],
            "email": credentials.email,
            "mfa_required": False
        }
        
        access_token = jwt_service.create_access_token(token_data)
        
        print(f"Token generated for user: {user_data['user_id']}")
        
        return AuthResponse(
            success=True,
            message="Login successful",
            token=Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=30 * 60,
                requires_mfa=False
            )
        )
    
    async def register(self, user_data: dict, session: Session) -> dict:
        """Register a new user with database audit logging"""
        try:
            success, result = await user_client.create_user({
                "email": user_data["email"],
                "password": user_data["password"],
                "full_name": user_data.get("full_name", user_data["email"]) 
            })
            
            if success:
                await self._log_audit_event(
                    user_id=result["id"],
                    event_type="user_registered",
                    details=f"New user registered: {user_data['email']}",
                    ip_address="unknown"
                )
                
                return {
                    "success": True,
                    "message": "User registered successfully",
                    "user": result
                }
            else:
                raise HTTPException(
                    status_code=400,
                    detail=result if isinstance(result, str) else "Registration failed"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Registration error: {str(e)}"
            )
    
    async def _log_audit_event(self, user_id: str, event_type: str, details: str, ip_address: str = "unknown"):
        """Helper method to log security events to audit service via database"""
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    "http://audit-service:8004/events",
                    json={
                        "user_id": user_id,
                        "event_type": event_type,
                        "details": details,
                        "ip_address": ip_address,
                        "user_agent": "auth-service"
                    }
                )
        except Exception as e:
            print(f"Failed to log audit event: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt with proper length handling"""
        try:
            password_bytes = password.encode('utf-8')
            if len(password_bytes) > 72:
                password_bytes = password_bytes[:72]
            
            salt = bcrypt_lib.gensalt()
            hashed = bcrypt_lib.hashpw(password_bytes, salt)
            return hashed.decode('utf-8')
        except Exception as e:
            print(f"Error hashing password: {e}")
            raise HTTPException(status_code=500, detail="Password hashing failed")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password using bcrypt with proper length handling"""
        try:
            password_bytes = plain_password.encode('utf-8')
            if len(password_bytes) > 72:
                password_bytes = password_bytes[:72]
            
            if isinstance(hashed_password, str):
                hashed_bytes = hashed_password.encode('utf-8')
            else:
                hashed_bytes = hashed_password
                
            return bcrypt_lib.checkpw(password_bytes, hashed_bytes)
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False

auth_service = AuthService()