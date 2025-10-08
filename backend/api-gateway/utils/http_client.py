import httpx
from fastapi import HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class HTTPClient:
    """HTTP client for service-to-service communication"""
    
    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
    
    async def forward_request(
        self, 
        method: str, 
        url: str, 
        headers: Dict[str, str], 
        content: bytes
    ) -> Dict[str, Any]:
        """Forward request to target service"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    content=content,
                    timeout=self.timeout
                )
                logger.info(f"Forwarded to {url} - Status: {response.status_code}")
                return response.json()
                
            except httpx.ConnectError:
                logger.error(f"Service connection failed: {url}")
                raise HTTPException(status_code=503, detail="Service unavailable")
            except httpx.TimeoutException:
                logger.error(f"Service timeout: {url}")
                raise HTTPException(status_code=504, detail="Service timeout")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")

http_client = HTTPClient()