from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from shift_service import models, schemas, crud
from shift_service.api import deps
from typing import List
from uuid import UUID

router = APIRouter()


@router.get("", response_model=List[schemas.User])
def get_users(
    offset: int = 0, limit: int = 10, session: Session = Depends(deps.get_session)
):
    query = crud.get_resources(
        session=session, model=models.User, offset=offset, limit=limit
    )
    return query.all()


@router.post("", response_model=schemas.User)
def create_user(user: schemas.UserCreate, session: Session = Depends(deps.get_session)):
    user_exist = crud.get_user_email(session, user.email)
    if user_exist is not None:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="User already exists"
        )
    return crud.create_user(session, user)


@router.delete("")
def delete_users(
    user_id: UUID,
    session: Session = Depends(deps.get_session),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    if current_user.level != models.UserLevel.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed to delete users",
        )
    user = crud.get_resource(session, models.User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    email = user.email
    crud.delete_resource(session, user)
    return {"message": f"user {email} has been deleted"}


@router.put("", response_model=schemas.User)
def edit_user(
    user_id: UUID,
    user: schemas.UserUpdate,
    session: Session = Depends(deps.get_session),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    if current_user.level != models.UserLevel.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed to edit users",
        )
    curr_user = crud.get_resource(session, models.User, user_id)
    if curr_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    curr_user = crud.edit_resource(session, curr_user, **user.dict(exclude_unset=True))
    return curr_user


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: UUID, session: Session = Depends(deps.get_session)):
    user = crud.get_resource(session, models.User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    return user
