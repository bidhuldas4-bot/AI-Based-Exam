from sqlalchemy.orm import Session
from models import Contact

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def create_contact(db: Session, name: str, email: str, mobile: int):
    db_contact = Contact(name=name, email=email, mobile=mobile)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact