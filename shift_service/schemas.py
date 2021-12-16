from uuid import uuid4
from pydantic import BaseModel, EmailStr, UUID4
from shift_service.models import UserLevel
from typing import List, Optional
from datetime import datetime


class BaseShift(BaseModel):
    id: int


class Shift(BaseShift):
    start_time: datetime
    end_time: datetime

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    id: UUID4


class User(BaseUser):
    level: UserLevel
    email: EmailStr
    shifts: List[Shift]

    class Config:
        orm_mode = True


class UserPass(BaseUser):
    email: EmailStr
    hashed_password: str

    class Config:
        orm_mode = True


class ShiftUpdate(BaseModel):
    start_time: datetime
    end_time: datetime


class UserUpdate(BaseModel):
    level: Optional[UserLevel]
    email: Optional[EmailStr]


class ShiftCreate(ShiftUpdate):
    pass


class UserCreate(BaseUser):
    id: UUID4 = uuid4()
    level: UserLevel
    email: EmailStr
    password: str
