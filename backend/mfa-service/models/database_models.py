from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class MFASecretDB(SQLModel, table=True):
    __tablename__ = "mfa_secrets"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, unique=True)
    secret: str
    is_enabled: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)