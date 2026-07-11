import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Fetch raw environment string securely
raw_url = os.getenv("DATABASE_URL", "")

# 2. Automate driver formatting injection to prevent authentication drops
if raw_url.startswith("postgresql://"):
    DATABASE_URL = raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)
else:
    DATABASE_URL = raw_url

# 3. Initialize engine with strict connection tracking parameters
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # Automatically re-verify broken pooler connections
    pool_recycle=1800        # Reset connection sockets every 30 minutes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
