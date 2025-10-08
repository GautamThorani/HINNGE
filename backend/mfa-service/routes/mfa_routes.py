from fastapi import APIRouter, Depends
from sqlmodel import Session

from services.mfa_service import mfa_service
from database.session import get_db_session
from models.mfa_models import MFAStatus, MFASetupResponse, MFAVerifyRequest, MFAVerifyResponse

router = APIRouter()

@router.get("/health")
async def health_check(session: Session = Depends(get_db_session)):
    """Health check endpoint"""
    try:
        from sqlmodel import text
        session.exec(text("SELECT 1"))
        return {"status": "healthy", "service": "mfa-service", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "service": "mfa-service", "database": "disconnected", "error": str(e)}

@router.get("/status/{user_id}", response_model=MFAStatus)
async def get_mfa_status(user_id: str, session: Session = Depends(get_db_session)):
    """Get MFA status for user"""
    return mfa_service.get_mfa_status(user_id, session)

@router.post("/setup/{user_id}", response_model=MFASetupResponse)
async def setup_mfa(user_id: str, session: Session = Depends(get_db_session)):
    """Setup MFA for user"""
    return mfa_service.setup_mfa(user_id, session)

@router.post("/verify", response_model=MFAVerifyResponse)
async def verify_mfa(request: MFAVerifyRequest, session: Session = Depends(get_db_session)):
    """Verify MFA token"""
    return mfa_service.verify_mfa(request.user_id, request.token, session)

@router.post("/enable/{user_id}")
async def enable_mfa(user_id: str, session: Session = Depends(get_db_session)):
    """Enable MFA for user (after successful verification)"""
    return mfa_service.enable_mfa(user_id, session)

@router.post("/disable/{user_id}")
async def disable_mfa(user_id: str, session: Session = Depends(get_db_session)):
    """Disable MFA for user"""
    return mfa_service.disable_mfa(user_id, session)

@router.delete("/reset/{user_id}")
async def reset_mfa(user_id: str, session: Session = Depends(get_db_session)):
    """Reset MFA for user"""
    return mfa_service.reset_mfa(user_id, session)