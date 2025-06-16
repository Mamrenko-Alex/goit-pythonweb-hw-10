from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
import crud
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Контактна Книга API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contacts/", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)


@app.get("/contacts/", response_model=List[schemas.ContactResponse])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_contacts(db, skip, limit)


@app.get("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact_by_id(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return contact


@app.put("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    updated = crud.update_contact(db, contact_id, contact)
    if updated is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return updated


@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_contact(db, contact_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return {"ok": True}


@app.get("/search/", response_model=List[schemas.ContactResponse])
def search(query: str, db: Session = Depends(get_db)):
    return crud.search_contacts(db, query)


@app.get("/birthdays/", response_model=List[schemas.ContactResponse])
def birthdays(db: Session = Depends(get_db)):
    return crud.upcoming_birthdays(db)
