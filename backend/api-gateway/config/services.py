import os

SERVICES = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001"),
    "users": os.getenv("USER_SERVICE_URL", "http://user-service:8002"), 
    "mfa": os.getenv("MFA_SERVICE_URL", "http://mfa-service:8003"),
    "audit": os.getenv("AUDIT_SERVICE_URL", "http://audit-service:8004")
}

def get_service_url(service_name: str) -> str:
    """Get service URL by name"""
    return SERVICES.get(service_name)

def is_service_available(service_name: str) -> bool:
    """Check if service exists in registry"""
    return service_name in SERVICES