from sqlmodel import Session, select
from typing import List, Optional, Dict
import uuid
from datetime import datetime

from models.database_models import AuditEventDB
from models.audit_models import AuditEvent

class AuditRepository:
    """Repository for audit database operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        return f"event_{uuid.uuid4().hex[:8]}"
    
    def log_event(self, event: AuditEvent) -> str:
        """Log a security event to database"""
        event_db = AuditEventDB(
            event_id=self._generate_event_id(),
            user_id=event.user_id,
            event_type=event.event_type,
            details=event.details,
            ip_address=event.ip_address,
            user_agent=event.user_agent,
            timestamp=datetime.fromisoformat(event.timestamp) if event.timestamp else datetime.utcnow()
        )
        
        self.session.add(event_db)
        self.session.commit()
        self.session.refresh(event_db)
        
        print(f"AUDIT EVENT LOGGED: {event_db.event_id} - {event_db.event_type}")
        return event_db.event_id
    
    def get_events(
        self, 
        user_id: Optional[str] = None, 
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[AuditEventDB]:
        """Get audit events with optional filtering"""
        query = select(AuditEventDB)
        
        if user_id:
            query = query.where(AuditEventDB.user_id == user_id)
        
        if event_type:
            query = query.where(AuditEventDB.event_type == event_type)
        
        query = query.order_by(AuditEventDB.timestamp.desc()).limit(limit)
        return self.session.exec(query).all()
    
    def query_events(self, query_params: Dict) -> List[AuditEventDB]:
        """Query audit events with advanced filtering"""
        query = select(AuditEventDB)
        
        if query_params.get("user_id"):
            query = query.where(AuditEventDB.user_id == query_params["user_id"])
        
        if query_params.get("event_type"):
            query = query.where(AuditEventDB.event_type == query_params["event_type"])
        
        if query_params.get("start_time"):
            start_time = datetime.fromisoformat(query_params["start_time"])
            query = query.where(AuditEventDB.timestamp >= start_time)
        
        if query_params.get("end_time"):
            end_time = datetime.fromisoformat(query_params["end_time"])
            query = query.where(AuditEventDB.timestamp <= end_time)
        
        query = query.order_by(AuditEventDB.timestamp.desc())
        return self.session.exec(query).all()
    
    def get_user_events(self, user_id: str, limit: int = 50) -> List[AuditEventDB]:
        """Get audit events for a specific user"""
        query = select(AuditEventDB).where(
            AuditEventDB.user_id == user_id
        ).order_by(
            AuditEventDB.timestamp.desc()
        ).limit(limit)
        
        return self.session.exec(query).all()
    
    def get_event_types(self) -> List[str]:
        """Get all unique event types"""
        events = self.session.exec(select(AuditEventDB)).all()
        return sorted(list(set(event.event_type for event in events)))
    
    def get_stats(self) -> Dict:
        """Get audit statistics"""
        events = self.session.exec(select(AuditEventDB)).all()
        
        total_events = len(events)
        unique_users = len(set(event.user_id for event in events))
        event_types = {}
        
        for event in events:
            event_type = event.event_type
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        latest_event = events[0] if events else None
        
        return {
            "total_events": total_events,
            "unique_users": unique_users,
            "events_by_type": event_types,
            "latest_event": latest_event
        }