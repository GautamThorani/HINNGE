from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class RefreshTokenDB(SQLModel, table=True):
    __tablename__ = "refresh_tokens"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    token_hash: str = Field(unique=True)
    expires_at: datetime
    is_revoked: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)