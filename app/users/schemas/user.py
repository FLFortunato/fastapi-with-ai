from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    lastName: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserOutput(BaseModel):
    name: str
    email: str
    lastName: str


class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
