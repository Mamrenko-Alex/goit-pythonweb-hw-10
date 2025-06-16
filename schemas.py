from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    birthday: Optional[date] = None


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True
