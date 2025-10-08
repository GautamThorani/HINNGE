from typing import Dict, Optional

class MFADatabase:
    """In-memory MFA database for demo purposes"""
    
    def __init__(self):
        self.mfa_secrets: Dict[str, str] = {} 
        self.mfa_status: Dict[str, bool] = {}  
    
    def get_secret(self, user_id: str) -> Optional[str]:
        """Get MFA secret for user"""
        return self.mfa_secrets.get(user_id)
    
    def set_secret(self, user_id: str, secret: str) -> None:
        """Set MFA secret for user"""
        self.mfa_secrets[user_id] = secret
    
    def get_status(self, user_id: str) -> bool:
        """Get MFA status for user"""
        return self.mfa_status.get(user_id, False)
    
    def set_status(self, user_id: str, enabled: bool) -> None:
        """Set MFA status for user"""
        self.mfa_status[user_id] = enabled
    
    def delete_user(self, user_id: str) -> None:
        """Remove user MFA data"""
        if user_id in self.mfa_secrets:
            del self.mfa_secrets[user_id]
        if user_id in self.mfa_status:
            del self.mfa_status[user_id]
    
    def user_exists(self, user_id: str) -> bool:
        """Check if user has MFA data"""
        return user_id in self.mfa_secrets

mfa_db = MFADatabase()