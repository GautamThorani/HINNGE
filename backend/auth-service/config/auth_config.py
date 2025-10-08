import os
from datetime import timedelta

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "hennge-demo-secret-key-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

USER_SERVICE_URL = "http://user-service:8002"

def get_access_token_expires():
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

def get_temp_token_expires():
    return timedelta(minutes=5) 