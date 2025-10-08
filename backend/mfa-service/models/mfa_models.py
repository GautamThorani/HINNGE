from pydantic import BaseModel

class MFAStatus(BaseModel):
    mfa_enabled: bool
    user_id: str

class MFASetupResponse(BaseModel):
    success: bool
    secret: str
    qr_code: str  
    provisioning_uri: str

class MFAVerifyRequest(BaseModel):
    user_id: str
    token: str

class MFAVerifyResponse(BaseModel):
    success: bool
    valid: bool