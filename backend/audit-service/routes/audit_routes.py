from fastapi import APIRouter, Depends
from typing import List 
from sqlmodel import Session

from services.audit_service import audit_service
from database.session import get_db_session
from models.audit_models import AuditEvent, AuditEventResponse, AuditQuery, AuditStats

router = APIRouter()

@router.get("/health")
async def health_check(session: Session = Depends(get_db_session)):
    """Health check endpoint"""
    try:
        from sqlmodel import text
        session.exec(text("SELECT 1"))
        return {"status": "healthy", "service": "audit-service", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "service": "audit-service", "database": "disconnected", "error": str(e)}

@router.post("/events")
async def log_event(event: AuditEvent, session: Session = Depends(get_db_session)):
    """Log a security event"""
    return audit_service.log_event(event, session)

@router.get("/events", response_model=List[AuditEventResponse])
async def get_events(
    user_id: str = None,
    event_type: str = None,
    limit: int = 100,
    session: Session = Depends(get_db_session)
):
    """Get audit events with optional filtering"""
    return audit_service.get_events(user_id, event_type, limit, session)

@router.post("/events/query")
async def query_events(query: AuditQuery, session: Session = Depends(get_db_session)):
    """Query audit events with advanced filtering"""
    return audit_service.query_events(query, session)

@router.get("/events/user/{user_id}")
async def get_user_events(user_id: str, limit: int = 50, session: Session = Depends(get_db_session)):
    """Get audit events for a specific user"""
    return audit_service.get_user_events(user_id, limit, session)

@router.get("/events/types")
async def get_event_types(session: Session = Depends(get_db_session)):
    """Get all unique event types"""
    return audit_service.get_event_types(session)

@router.get("/stats", response_model=AuditStats)
async def get_audit_stats(session: Session = Depends(get_db_session)):
    """Get audit statistics"""
    return audit_service.get_stats(session)