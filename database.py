"""
database.py
-----------
SQLAlchemy engine/session setup. Uses SQLite by default (zero setup,
works out of the box). To switch to MySQL later, just change DATABASE_URL
in your .env file to something like:
    mysql+pymysql://user:password@localhost/plant_recognition
and `pip install pymysql`.
"""
 
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
 
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./plant_recognition.db")
 
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
 
 
def get_db():
    """FastAPI dependency — yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 