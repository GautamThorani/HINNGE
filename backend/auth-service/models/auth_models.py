from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    requires_mfa: bool = False

class TokenData(BaseModel):
    user_id: str
    email: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    token: Optional[Token] = None

class TokenVerification(BaseModel):
    valid: bool
    user: Optional[TokenData] = None

class UserRegistration(BaseModel):
    email: str
    password: str
    full_name: str