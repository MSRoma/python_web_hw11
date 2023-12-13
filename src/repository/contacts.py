from typing import List
from datetime import date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import  or_, extract

from src.database.models import Contact
from src.schemas import ContactModel
from sqlalchemy import select


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    result =  db.query(Contact).offset(skip).limit(limit).all()
    return db.query(Contact).offset(skip).limit(limit).all()
   
async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def get_contact_firstname(firstname: str ,lastname: str,email: str  ,skip: int, limit: int,  db: Session):
    return db.query(Contact).where((or_(Contact.firstname == firstname),(Contact.lastname == lastname),(Contact.email == email))).\
            offset(skip).limit(limit).all()   

async def get_contact_birthday(skip: int, limit: int,  db: Session):
    date_now = date.today()
    year_now = date_now.year
    diff = date_now + timedelta(days = 7)
    date_to = date(year=year_now, month=diff.month, day=diff.day)

    result = db.query(Contact).\
        filter((extract('month', Contact.databirthday) >= date_now.month)).\
        filter((extract('month', Contact.databirthday) <= date_to.month)).\
        filter(extract('day', Contact.databirthday) >= date_now.day).\
        filter(extract('day', Contact.databirthday) <= date_to.day).\
        offset(skip).limit(limit).all()
    return result  

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



