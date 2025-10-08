from fastapi import HTTPException
import pyotp
from sqlmodel import Session

from database.mfa_repository import MFARepository
from services.qr_service import qr_service
from models.mfa_models import MFAStatus, MFASetupResponse, MFAVerifyResponse

class MFAService:
    """MFA service handling TOTP business logic with database"""
    
    @staticmethod
    def generate_secret() -> str:
        """Generate a new TOTP secret"""
        return pyotp.random_base32()
    
    @staticmethod
    def verify_totp(secret: str, token: str) -> bool:
        """Verify TOTP token"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
    
    @staticmethod
    def get_mfa_status(user_id: str, session: Session) -> MFAStatus:
        """Get MFA status for user"""
        repository = MFARepository(session)
        enabled = repository.get_status(user_id)
        return MFAStatus(mfa_enabled=enabled, user_id=user_id)
    
    @staticmethod
    def setup_mfa(user_id: str, session: Session) -> MFASetupResponse:
        """Setup MFA for user"""
        secret = MFAService.generate_secret()
        
        repository = MFARepository(session)
        repository.set_secret(user_id, secret, False)

        qr_code, provisioning_uri = qr_service.generate_qr_code(secret, f"user_{user_id}")
        
        print(f"MFA setup for user {user_id} - secret stored in database")
        
        return MFASetupResponse(
            success=True,
            secret=secret,
            qr_code=qr_code,
            provisioning_uri=provisioning_uri
        )
    
    @staticmethod
    def verify_mfa(user_id: str, token: str, session: Session) -> MFAVerifyResponse:
        """Verify MFA token"""
        repository = MFARepository(session)
        mfa_data = repository.get_secret(user_id)
        
        if not mfa_data:
            raise HTTPException(status_code=404, detail="MFA not setup for user")
        
        is_valid = MFAService.verify_totp(mfa_data.secret, token)
        
        if is_valid and not mfa_data.is_enabled:
            repository.set_status(user_id, True)
            print(f"MFA enabled for user {user_id} after successful verification")
        
        return MFAVerifyResponse(
            success=True,
            valid=is_valid
        )
    
    @staticmethod
    def enable_mfa(user_id: str, session: Session) -> dict:
        """Enable MFA for user (after successful verification)"""
        repository = MFARepository(session)
        mfa_data = repository.get_secret(user_id)
        
        if not mfa_data:
            raise HTTPException(status_code=404, detail="MFA not setup for user")
        
        repository.set_status(user_id, True)
        print(f"MFA manually enabled for user {user_id}")
        
        return {"success": True, "message": "MFA enabled"}
    
    @staticmethod
    def disable_mfa(user_id: str, session: Session) -> dict:
        """Disable MFA for user"""
        repository = MFARepository(session)
        repository.set_status(user_id, False)
        print(f"MFA disabled for user {user_id}")
        
        return {"success": True, "message": "MFA disabled"}
    
    @staticmethod
    def reset_mfa(user_id: str, session: Session) -> dict:
        """Reset MFA for user"""
        repository = MFARepository(session)
        deleted = repository.delete_user(user_id)
        
        if deleted:
            print(f"MFA reset for user {user_id}")
            return {"success": True, "message": "MFA reset"}
        else:
            raise HTTPException(status_code=404, detail="MFA not setup for user")

mfa_service = MFAService()