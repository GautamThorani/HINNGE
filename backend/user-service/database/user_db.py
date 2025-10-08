from typing import Dict, List, Optional
import uuid
from datetime import datetime
import bcrypt  

from models.user_models import UserCreate
class UserDatabase:
    """In-memory user database with proper password hashing"""
    
    def __init__(self):
        self.users: Dict[str, dict] = {}
        self.user_by_email: Dict[str, str] = {}
    
    def _create_user_id(self) -> str:
        return f"user_{uuid.uuid4().hex[:8]}"
    
    def _get_current_timestamp(self) -> str:
        return datetime.utcnow().isoformat()
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash using bcrypt"""
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
    
    def create_user(self, user_data: UserCreate) -> dict:
        """Create a new user with hashed password"""
        if user_data.email in self.user_by_email:
            raise ValueError("User already exists")
        
        hashed_password = self._hash_password(user_data.password)

        user_id = self._create_user_id()
        user = {
            "id": user_id,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "password": hashed_password, 
            "created_at": self._get_current_timestamp(),
            "is_active": True
        }
        
        self.users[user_id] = user
        self.user_by_email[user_data.email] = user_id
        
        print(f" User created: {user_data.email} (password hashed)")
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[dict]:
        if email not in self.user_by_email:
            return None
        user_id = self.user_by_email[email]
        return self.users.get(user_id)
    
    def get_all_users(self) -> List[dict]:
        return list(self.users.values())
    
    def verify_credentials(self, email: str, password: str) -> Optional[dict]:
        """Verify user credentials using hashed password comparison"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        if not self._verify_password(password, user["password"]):
            return None
        
        return user
    
    def user_exists(self, email: str) -> bool:
        return email in self.user_by_email

user_db = UserDatabase()