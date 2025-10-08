from typing import List, Optional
from sqlmodel import Session

from database.audit_repository import AuditRepository
from models.audit_models import AuditEvent, AuditEventResponse, AuditQuery, AuditStats

class AuditService:
    """Audit service handling security event logging and queries with database"""
    
    @staticmethod
    def log_event(event: AuditEvent, session: Session) -> dict:
        """Log a security event to database"""
        repository = AuditRepository(session)
        event_id = repository.log_event(event)
        return {"success": True, "event_id": event_id}
    
    @staticmethod
    def get_events(
        user_id: Optional[str] = None, 
        event_type: Optional[str] = None,
        limit: int = 100,
        session: Session = None
    ) -> List[AuditEventResponse]:
        """Get audit events with optional filtering"""
        repository = AuditRepository(session)
        events = repository.get_events(user_id, event_type, limit)
        return [AuditService._to_event_response(event) for event in events]
    
    @staticmethod
    def query_events(query: AuditQuery, session: Session) -> dict:
        """Query audit events with advanced filtering"""
        repository = AuditRepository(session)
        events = repository.query_events(query.dict())
        return {
            "count": len(events),
            "events": [AuditService._to_event_response(event) for event in events]
        }
    
    @staticmethod
    def get_user_events(user_id: str, limit: int = 50, session: Session = None) -> dict:
        """Get audit events for a specific user"""
        repository = AuditRepository(session)
        events = repository.get_user_events(user_id, limit)
        return {
            "user_id": user_id,
            "total_events": len(events),
            "events": [AuditService._to_event_response(event) for event in events]
        }
    
    @staticmethod
    def get_event_types(session: Session) -> dict:
        """Get all unique event types"""
        repository = AuditRepository(session)
        event_types = repository.get_event_types()
        return {"event_types": event_types}
    
    @staticmethod
    def get_stats(session: Session) -> AuditStats:
        """Get audit statistics"""
        repository = AuditRepository(session)
        stats = repository.get_stats()
        
        latest_event = None
        if stats["latest_event"]:
            latest_event = AuditService._to_event_response(stats["latest_event"])
        
        return AuditStats(
            total_events=stats["total_events"],
            unique_users=stats["unique_users"],
            events_by_type=stats["events_by_type"],
            latest_event=latest_event
        )
    
    @staticmethod
    def _to_event_response(event) -> AuditEventResponse:
        """Convert database event to response model"""
        return AuditEventResponse(
            id=event.event_id,
            user_id=event.user_id,
            event_type=event.event_type,
            details=event.details,
            timestamp=event.timestamp.isoformat(),
            ip_address=event.ip_address,
            user_agent=event.user_agent
        )

audit_service = AuditService()