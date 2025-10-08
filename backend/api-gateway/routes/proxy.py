from fastapi import APIRouter, HTTPException, Request
from typing import Any

from config.services import get_service_url, is_service_available
from utils.http_client import http_client

router = APIRouter()

@router.api_route("/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_request(service_name: str, path: str, request: Request) -> Any:
    """
    Proxy requests to appropriate microservices
    """
    if not is_service_available(service_name):
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    service_url = get_service_url(service_name)
    target_url = f"{service_url}/{path}"
    
    response_data = await http_client.forward_request(
        method=request.method,
        url=target_url,
        headers=dict(request.headers),
        content=await request.body()
    )
    
    return response_data

@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "api-gateway",
        "message": "API Gateway is running"
    }