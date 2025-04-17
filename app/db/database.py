from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

# Example for PostgreSQL (e.g. Supabase)
DATABASE_URL = os.getenv("DATABASE_URL")  # e.g. "postgresql://user:pass@host:port/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# For Alembic migration use
def get_metadata():
    return Base.metadata