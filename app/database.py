from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi_users.db import SQLAlchemyUserDatabase
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from app.models import UserTable

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base: DeclarativeMeta = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_db(session: Session = Depends(get_db)):
    yield SQLAlchemyUserDatabase(UserTable, session)
