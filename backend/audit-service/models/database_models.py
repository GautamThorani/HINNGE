from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class AuditEventDB(SQLModel, table=True):
    __tablename__ = "audit_events"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: str = Field(index=True, unique=True)  
    user_id: str = Field(index=True)
    event_type: str = Field(index=True)
    details: str
    ip_address: str = "unknown"
    user_agent: str = "unknown"
    timestamp: datetime = Field(default_factory=datetime.utcnow)