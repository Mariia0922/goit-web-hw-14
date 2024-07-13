from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Contact, ContactCreate, ContactUpdate
from app.main import fastapi_users, UserRead
from typing import List

router = APIRouter()

@router.post("/", response_model=ContactCreate)
async def create_contact(
    contact: ContactCreate, 
    db: Session = Depends(get_db), 
    user: UserRead = Depends(fastapi_users.current_user)
):
    db_contact = Contact(**contact.dict(), owner_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/", response_model=List[ContactCreate])
async def read_contacts(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    user: UserRead = Depends(fastapi_users.current_user)
):
    contacts = db.query(Contact).filter(Contact.owner_id == user.id).offset(skip).limit(limit).all()
    return contacts
