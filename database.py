import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# IMPORTANT: Replace this string with your real connection URL from your Neon dashboard
DATABASE_URL = "postgresql://neondb_owner:npg_niFcuI4MR8wL@ep-fancy-sun-aqkf0vbs-pooler.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
