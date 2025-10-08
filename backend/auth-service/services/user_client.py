import httpx
from fastapi import HTTPException

from config.auth_config import USER_SERVICE_URL

class UserClient:
    """Client for communicating with User Service"""
    
    @staticmethod
    async def get_user_by_email(email: str):
        """Get user from user service by email"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{USER_SERVICE_URL}/email/{email}")
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    @staticmethod
    async def verify_user_credentials(email: str, password: str):
        """Verify user credentials with user service"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{USER_SERVICE_URL}/verify-login",
                    json={"email": email, "password": password}
                )
                return response.status_code == 200, response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error verifying credentials: {e}")
            return False, None
    
    @staticmethod
    async def create_user(user_data: dict):
        """Create user in user service"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{USER_SERVICE_URL}/users",
                    json=user_data
                )
                return response.status_code == 200, response.json() if response.status_code == 200 else response.text
        except Exception as e:
            print(f"Error creating user: {e}")
            return False, str(e)

user_client = UserClient()