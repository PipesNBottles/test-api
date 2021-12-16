from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from shift_service import models, schemas, crud
from shift_service.api import deps
from datetime import time
from typing import Optional, List
import pytz

router = APIRouter()
utc = pytz.UTC


@router.get("", response_model=List[schemas.Shift])
def list_shifts(
    start_time: Optional[time] = None,
    end_time: Optional[time] = None,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(deps.get_session),
):
    kwargs = {}
    if start_time:
        kwargs["start_time"] = start_time
    if end_time:
        kwargs["end_time"] = end_time
    query = (
        session.query(models.Shift)
        .filter_by(**kwargs)
        .order_by(models.Shift.start_time)
        .offset(offset)
        .limit(limit)
    )
    return query.all()


@router.get("/{shift_id}", response_model=schemas.Shift)
def get_shift(shift_id: int, session: Session = Depends(deps.get_session)):
    shift = crud.get_resource(session, models.Shift, shift_id)
    if shift is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shift does not exist"
        )
    return shift


@router.post("", response_model=schemas.Shift)
def create_shift(
    user_id: UUID,
    new_shift: schemas.ShiftCreate,
    session: Session = Depends(deps.get_session),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    if current_user.level != models.UserLevel.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed to make shifts",
        )
    user = crud.get_resource(session, models.User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
        )
    for shift in user.shifts:
        if (
            utc.localize(new_shift.start_time) >= utc.localize(shift.start_time)
            and utc.localize(new_shift.start_time) <= utc.localize(shift.end_time)
            or utc.localize(new_shift.end_time) >= utc.localize(shift.start_time)
            and utc.localize(new_shift.end_time) <= utc.localize(shift.end_time)
            or utc.localize(new_shift.start_time) <= utc.localize(shift.start_time)
            and utc.localize(new_shift.end_time) >= utc.localize(shift.end_time)
        ):
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Shift cannot overlap existing shifts",
            )
    else:
        return crud.create_shift(session, {"user_id": user_id, **new_shift.dict()})


@router.put("/{user_id}/{shift_id}", response_model=schemas.Shift)
def edit_shift(
    shift_id: int,
    user_id: UUID,
    new_shift: schemas.ShiftUpdate,
    session: Session = Depends(deps.get_session),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    if current_user.level != models.UserLevel.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed to edit shifts",
        )
    curr_shift = crud.get_resource(session, models.Shift, shift_id)
    if curr_shift is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shift does not exist"
        )
    user = crud.get_resource(session, models.User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    for shift in user.shifts:
        if shift is curr_shift:
            continue
        if (
            new_shift.start_time >= utc.localize(shift.start_time)
            and new_shift.start_time <= utc.localize(shift.end_time)
            or new_shift.end_time >= utc.localize(shift.start_time)
            and new_shift.end_time <= utc.localize(shift.end_time)
            or utc.localize(new_shift.start_time) <= utc.localize(shift.start_time)
            and utc.localize(new_shift.end_time) >= utc.localize(shift.end_time)
        ):
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Shift cannot overlap existing shifts",
            )
    else:
        return crud.edit_resource(
            session, curr_shift, **{"user_id": user_id, **new_shift.dict()}
        )


@router.delete("")
def delete_shift(
    shift_id: int,
    session: Session = Depends(deps.get_session),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    if current_user.level != models.UserLevel.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed to delete shifts",
        )
    shift = crud.get_resource(session, models.Shift, shift_id)
    if shift is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shift does not exist"
        )
    crud.delete_resource(session, shift)
    return {"message": f"Shift {shift_id} has been deleted"}
