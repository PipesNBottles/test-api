from sqlalchemy.orm import query, Session
from shift_service import database
from fastapi import Depends, HTTPException, status
from shift_service import crud
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_session():
    try:
        db = database.local_session(query_cls=query.Query)
        yield db
    finally:
        db.close()


async def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    user = crud.get_user_email(session, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
