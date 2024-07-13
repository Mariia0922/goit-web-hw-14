from fastapi import APIRouter, Depends
from app.main import fastapi_users
from app.models import UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/",
    tags=["users"],
)
