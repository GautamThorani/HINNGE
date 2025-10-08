from fastapi import FastAPI
import logging

from middleware.cors import setup_cors
from routes.proxy import router as proxy_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="HENNGE API Gateway",
        description="Gateway for HENNGE Security Microservices",
        version="1.0.0"
    )
    

    setup_cors(app)
    
    app.include_router(proxy_router)
    
    logger.info("API Gateway started successfully")
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)