from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://hennge_user:hennge_password@postgres:5432/hennge_security")

engine = create_engine(DATABASE_URL, echo=True)

def get_db_session():
    """Dependency for FastAPI to get database session"""
    with Session(engine) as session:
        yield session