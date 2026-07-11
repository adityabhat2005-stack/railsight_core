import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# IMPORTANT: Replace this string with your real connection URL from your Neon dashboard
DATABASE_URL = "postgresql://user:password@ep-xxxx.neon.tech/neondb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
