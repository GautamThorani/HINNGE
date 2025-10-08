from typing import List, Dict, Optional
import uuid
from datetime import datetime

from models.audit_models import AuditEvent

class AuditDatabase:
    """In-memory audit database for demo purposes"""
    
    def __init__(self):
        self.audit_events: List[dict] = []
    
    def _create_event_id(self) -> str:
        """Generate unique event ID"""
        return f"event_{uuid.uuid4().hex[:8]}"
    
    def _get_current_timestamp(self) -> str:
        """Get current ISO timestamp"""
        return datetime.utcnow().isoformat()
    
    def log_event(self, event: AuditEvent) -> str:
        """Log a security event"""
        event_data = {
            "id": self._create_event_id(),
            "user_id": event.user_id,
            "event_type": event.event_type,
            "details": event.details,
            "timestamp": event.timestamp or self._get_current_timestamp(),
            "ip_address": event.ip_address,
            "user_agent": event.user_agent
        }
        
        self.audit_events.append(event_data)
        print(f"AUDIT: {event_data}") 
        return event_data["id"]
    
    def get_events(
        self, 
        user_id: Optional[str] = None, 
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[dict]:
        """Get audit events with optional filtering"""
        filtered_events = self.audit_events.copy()
        
        if user_id:
            filtered_events = [e for e in filtered_events if e["user_id"] == user_id]
        
        if event_type:
            filtered_events = [e for e in filtered_events if e["event_type"] == event_type]
        
        filtered_events.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return filtered_events[:limit]
    
    def query_events(self, query: Dict) -> List[dict]:
        """Query audit events with advanced filtering"""
        filtered_events = self.audit_events.copy()
        
        if query.get("user_id"):
            filtered_events = [e for e in filtered_events if e["user_id"] == query["user_id"]]
        
        if query.get("event_type"):
            filtered_events = [e for e in filtered_events if e["event_type"] == query["event_type"]]
        
        if query.get("start_time"):
            filtered_events = [e for e in filtered_events if e["timestamp"] >= query["start_time"]]
        
        if query.get("end_time"):
            filtered_events = [e for e in filtered_events if e["timestamp"] <= query["end_time"]]
        
        filtered_events.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return filtered_events
    
    def get_user_events(self, user_id: str, limit: int = 50) -> List[dict]:
        """Get audit events for a specific user"""
        user_events = [e for e in self.audit_events if e["user_id"] == user_id]
        user_events.sort(key=lambda x: x["timestamp"], reverse=True)
        return user_events[:limit]
    
    def get_event_types(self) -> List[str]:
        """Get all unique event types"""
        return list(set(event["event_type"] for event in self.audit_events))
    
    def get_stats(self) -> Dict:
        """Get audit statistics"""
        total_events = len(self.audit_events)
        unique_users = len(set(event["user_id"] for event in self.audit_events))
        event_types = {}
        
        for event in self.audit_events:
            event_type = event["event_type"]
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        latest_event = self.audit_events[-1] if self.audit_events else None
        
        return {
            "total_events": total_events,
            "unique_users": unique_users,
            "events_by_type": event_types,
            "latest_event": latest_event
        }

audit_db = AuditDatabase()