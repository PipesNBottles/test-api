from enum import IntEnum
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType, EmailType
from libs.database import Base


class UserLevel(IntEnum):
    EMPLOYEE = 1


class User(Base):
    __tablename__ = "user"
    id = Column(UUIDType(binary=False), primary_key=True)
    level = Column(
        Enum(UserLevel, native_enum=False), default=UserLevel.EMPLOYEE, nullable=False
    )
    email = Column(EmailType(), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    shifts = relationship("Shift", cascade="all, delete-orphan", lazy="joined")


class Shift(Base):
    __tablename__ = "shift"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUIDType(binary=False), ForeignKey("user.id"))
    start_time = Column(DateTime(), nullable=False)
    end_time = Column(DateTime(), nullable=False)
