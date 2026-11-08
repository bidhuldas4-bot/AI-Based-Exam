from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Contact
from crud import get_contact, create_contact

app = FastAPI()

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contacts/")
async def create_contact_endpoint(name: str, email: str, mobile: int, db: Session = Depends(get_db)):
    return create_contact(db, name, email, mobile)

@app.get("/contacts/{contact_id}")
async def get_contact_endpoint(contact_id: int, db: Session = Depends(get_db)):
    contact = get_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}")
async def update_contact_endpoint(contact_id: int, name: str, email: str, mobile: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    contact.name = name
    contact.email = email
    contact.mobile = mobile
    db.commit()
    db.refresh(contact)
    
    return contact

@app.delete("/contacts/{contact_id}")
async def delete_contact_endpoint(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(contact)
    db.commit()
    
    return {"detail": "Contact deleted"}