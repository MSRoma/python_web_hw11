from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()

async def get_contact_firstname(contact_firstname: str, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.firstname==contact_firstname)


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(firstname=body.firstname, lastname=body.lastname, email=body.email, mobilenamber=body.mobilenamber, databirthday=body.databirthday, note=body.note )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact :
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.mobilenamber = body.mobilenamber
        contact.databirthday = body.databirthday
        contact.note = body.note
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session)  -> Contact :
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.delete(contact)
    db.commit()
    return contact