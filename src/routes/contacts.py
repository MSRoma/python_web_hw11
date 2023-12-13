from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse # ContactStatusUpdate
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/contacts/", response_model=List[ContactResponse],tags=["contacts"])
async def read_contacts_name_or_surname_or_email(firstname: str | None = None,lastname: str | None = None, email: str | None = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_firstname(firstname, lastname, email, skip, limit, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/birthday/", response_model=List[ContactResponse],tags=["contacts"])
async def read_contacts_birthday(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_birthday(skip, limit, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact



@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# @router.patch("/{contact_id}", response_model=ContactResponse)
# async def update_status_contact(body: ContactStatusUpdate, contact_id: int, db: Session = Depends(get_db)):
#     contact = await repository_contacts.update_status_contact(contact_id, body, db)
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
#     return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact