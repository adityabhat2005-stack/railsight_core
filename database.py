import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Uses env var with a hardcoded fallback to ensure connection
env_url = os.getenv("DATABASE_URL")
# Use valid Neon database connection string here
DATABASE_URL = env_url if env_url else "your_safe_fallback_url"

# Configures engine with safety parameters
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
