from sqlmodel import Session, select
from typing import Optional
from datetime import datetime 

from models.database_models import MFASecretDB

class MFARepository:
    """Repository for MFA database operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _get_current_timestamp(self): 
        """Get current timestamp"""
        return datetime.utcnow()
    
    def get_secret(self, user_id: str) -> Optional[MFASecretDB]:
        """Get MFA secret for user"""
        return self.session.exec(
            select(MFASecretDB).where(MFASecretDB.user_id == user_id)
        ).first()
    
    def set_secret(self, user_id: str, secret: str, is_enabled: bool = False) -> MFASecretDB:
        """Set MFA secret for user"""
        existing = self.get_secret(user_id)
        
        if existing:
            existing.secret = secret
            existing.is_enabled = is_enabled
            existing.updated_at = self._get_current_timestamp()  
        else:
            existing = MFASecretDB(
                user_id=user_id,
                secret=secret,
                is_enabled=is_enabled
            )
            self.session.add(existing)
        
        self.session.commit()
        self.session.refresh(existing)
        return existing
    
    def get_status(self, user_id: str) -> bool:
        """Get MFA status for user"""
        mfa_data = self.get_secret(user_id)
        return mfa_data.is_enabled if mfa_data else False
    
    def set_status(self, user_id: str, enabled: bool) -> Optional[MFASecretDB]:
        """Set MFA status for user"""
        mfa_data = self.get_secret(user_id)
        if not mfa_data:
            return None
        
        mfa_data.is_enabled = enabled
        mfa_data.updated_at = self._get_current_timestamp()  
        self.session.commit()
        self.session.refresh(mfa_data)
        return mfa_data
    
    def delete_user(self, user_id: str) -> bool:
        """Remove user MFA data"""
        mfa_data = self.get_secret(user_id)
        if mfa_data:
            self.session.delete(mfa_data)
            self.session.commit()
            return True
        return False
    
    def user_exists(self, user_id: str) -> bool:
        """Check if user has MFA data"""
        return self.get_secret(user_id) is not None