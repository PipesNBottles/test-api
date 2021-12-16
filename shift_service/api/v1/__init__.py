from fastapi import APIRouter

from shift_service.api.v1.endpoints import shifts, users

api_router = APIRouter()

api_router.include_router(shifts.router, prefix="/shifts", tags=["shifts"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
