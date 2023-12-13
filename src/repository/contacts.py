from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_

from src.database.models import Contact
from src.schemas import ContactModel
from sqlalchemy import select


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    result =  db.query(Contact).offset(skip).limit(limit).all()
    print(f"))))))))))))))))))))))))))))))))))))))){result}")

    db.query(Contact).offset(skip).limit(limit).all()
    return result
   


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def get_contact_firstname(firstname:str  ,  db: Session):
    print(f"=========================================================={firstname}")
    result = db.query(Contact).filter(Contact.firstname == firstname).all()
    print(f"((((((((((((((((((((((((((((((((((((((((({result}")
    return result
    #return db.query(Contact).filter(Contact.firstname.like("%1%"))
    # if firstname:
    #     field = Contact.firstname
    #     value = firstname
    # elif lastname:
    #     field = Contact.lastname
    #     value =  lastname
    # elif email:
    #     field = Contact. email
    #     value =  email
    #return db.query(Contact).filter(Contact.firstname == firstname).count()
    
     


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



#)))))))))))))))))))))))))))))))))))))))[<src.database.models.Contact object at 0x0000017343CEDE90>, <src.database.models.Contact object at 0x0000017341D483D0>, <src.database.models.Contact object at 0x0000017343CEDF50>]
#((((((((((((((((((((((((((((((((((((((([<src.database.models.Contact object at 0x000001F92DA777D0>, <src.database.models.Contact object at 0x000001F92DA77850>]