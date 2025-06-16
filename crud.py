from sqlalchemy.orm import Session
from models import Contact
from schemas import ContactCreate, ContactUpdate
from datetime import date, timedelta
from datetime import datetime


def get_all_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact_by_id(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict(), created_at=datetime.utcnow())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, updated_data: ContactUpdate):
    contact = get_contact_by_id(db, contact_id)
    if contact:
        updated_fields = updated_data.dict(
            exclude_unset=True)  # 💡 Только переданные поля
        for key, value in updated_fields.items():
            setattr(contact, key, value)
        db.commit()
        db.refresh(contact)
    return contact


def delete_contact(db: Session, contact_id: int):
    contact = get_contact_by_id(db, contact_id)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


def search_contacts(db: Session, query: str):
    return db.query(Contact).filter(
        (Contact.first_name.ilike(f"%{query}%")) |
        (Contact.last_name.ilike(f"%{query}%")) |
        (Contact.email.ilike(f"%{query}%"))
    ).all()


def upcoming_birthdays(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(
        Contact.birthday.between(today, next_week)
    ).all()
