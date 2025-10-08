from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AuditEvent(BaseModel):
    user_id: str
    event_type: str
    details: str
    timestamp: Optional[str] = None
    ip_address: str = "unknown"
    user_agent: str = "unknown"

class AuditEventResponse(BaseModel):
    id: str
    user_id: str
    event_type: str
    details: str
    timestamp: str
    ip_address: str

class AuditQuery(BaseModel):
    user_id: Optional[str] = None
    event_type: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class AuditStats(BaseModel):
    total_events: int
    unique_users: int
    events_by_type: dict
    latest_event: Optional[AuditEventResponse] = None