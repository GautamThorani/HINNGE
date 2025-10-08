from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status

from config.auth_config import SECRET_KEY, ALGORITHM, get_access_token_expires, get_temp_token_expires
from models.auth_models import TokenData

class JWTService:
    """Service for JWT token operations"""
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + get_access_token_expires()
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_temp_token(data: dict) -> str:
        """Create temporary token for MFA flow"""
        return JWTService.create_access_token(data, get_temp_token_expires())
    
    @staticmethod
    def verify_token(token: str) -> TokenData:
        """Verify JWT token and return token data"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("user_id")
            email: str = payload.get("email")
            
            if user_id is None or email is None:
                raise credentials_exception
                
            return TokenData(user_id=user_id, email=email)
        except JWTError:
            raise credentials_exception
    
    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode JWT token without verification (for internal use)"""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return {}

jwt_service = JWTService()