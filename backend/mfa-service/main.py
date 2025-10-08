from fastapi import FastAPI
import logging

from routes.mfa_routes import router as mfa_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="HENNGE MFA Service",
        description="Multi-Factor Authentication microservice for HENNGE Security",
        version="1.0.0"
    )

    app.include_router(mfa_router)
    
    logger.info("MFA Service started successfully")
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)