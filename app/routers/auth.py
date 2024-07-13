import os
from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy
from app.main import get_user_manager

router = APIRouter()

fastapi_users = FastAPIUsers(
    get_user_manager,
    [JWTStrategy(secret=os.getenv("SECRET"), lifetime_seconds=3600)],
)

router.include_router(
    fastapi_users.get_auth_router(JWTStrategy(secret=os.getenv("SECRET"), lifetime_seconds=3600)),
    prefix="/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(),
    prefix="/register",
    tags=["auth"],
)
