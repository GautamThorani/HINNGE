from sqlmodel import Session, select
from typing import List, Optional
import bcrypt
import uuid


from models.database_models import User
from models.user_models import UserCreate

class UserRepository:
    """Repository for database operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            password_bytes = plain_password.encode('utf-8')
            if len(password_bytes) > 72:
                password_bytes = password_bytes[:72]
            
            if isinstance(hashed_password, str):
                hashed_bytes = hashed_password.encode('utf-8')
            else:
                hashed_bytes = hashed_password
                
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False
    
    def _generate_user_id(self) -> str:
        """Generate unique user ID"""
        return f"user_{uuid.uuid4().hex[:8]}"
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user in database"""
        existing_user = self.session.exec(
            select(User).where(User.email == user_data.email)
        ).first()
        
        if existing_user:
            raise ValueError("User already exists")
        
        hashed_password = self._hash_password(user_data.password)
        
        user = User(
            user_id=self._generate_user_id(),
            email=user_data.email,
            full_name=user_data.full_name,
            password_hash=hashed_password,
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        print(f"User created in database: {user_data.email}")
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by user_id"""
        return self.session.exec(
            select(User).where(User.user_id == user_id)
        ).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.session.exec(
            select(User).where(User.email == email)
        ).first()
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self.session.exec(select(User)).all()
    
    def verify_credentials(self, email: str, password: str) -> Optional[User]:
        """Verify user credentials"""
        user = self.get_user_by_email(email)
        if not user or not user.is_active:
            return None
        
        if not self._verify_password(password, user.password_hash):
            return None
        
        return user