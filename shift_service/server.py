from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from shift_service import crud, security
from shift_service.api import deps
from starlette.middleware.cors import CORSMiddleware

from shift_service import settings
from shift_service.api.v1 import api_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/v1")


@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(deps.get_session),
):
    user = crud.get_user_email(session, form_data.username)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not security.check_password(
        form_data.password.encode(), user.hashed_password.encode()
    ):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.email, "token_type": "bearer"}


@app.get("/ping")
def health_check():
    """
    Endpoint to check whether the service is alive and ready for traffic
    """
    return {"message": "pong"}
