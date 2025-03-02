from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Define Base for models to inherit from
Base = declarative_base()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an engine for connecting to the database
engine = create_engine(DATABASE_URL)

# Create a session maker for interacting with the database
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
