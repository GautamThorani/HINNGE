from fastapi import Depends
from fastapi.security import HTTPBearer

from services.jwt_service import jwt_service
from models.auth_models import TokenData

security = HTTPBearer()

async def verify_token(token: str = Depends(security)) -> TokenData:
    """
    Dependency for verifying JWT token in protected routes
    """
    return jwt_service.verify_token(token.credentials)