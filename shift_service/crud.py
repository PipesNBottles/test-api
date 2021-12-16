from typing import Dict
from shift_service import schemas
from sqlalchemy.orm.session import Session
from shift_service.models import User, Shift
from shift_service.security import create_hash_pass


def get_resource(session: Session, model, id):
    return session.query(model).filter(model.id == id).one_or_none()


def get_resources(session: Session, model, offset: int, limit: int, **kwargs):
    return session.query(model).filter_by(**kwargs).offset(offset).limit(limit)


def delete_resource(session: Session, model):
    session.delete(model)
    session.commit()
    return


def edit_resource(session: Session, model, **kwargs):
    for key, value in kwargs.items():
        setattr(model, key, value)
    session.commit()
    return model


def create_user(session: Session, user: schemas.UserCreate):
    hashed_password = create_hash_pass(user.password.encode())
    db_user = User(
        **user.dict(exclude={"password"}), hashed_password=hashed_password.decode()
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def authenticate_user(session: Session, email: str, password: str):
    ...


def create_shift(session: Session, shift: Dict):
    db_shift = Shift(**shift)
    session.add(db_shift)
    session.commit()
    session.refresh(db_shift)
    return db_shift


def get_user_email(session: Session, email: str):
    return session.query(User).filter(User.email == email).one_or_none()
