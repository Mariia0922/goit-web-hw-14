import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.manager import BaseUserManager
from fastapi_users.password import PasswordHelper
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from typing import Optional
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from app.database import Base, engine, get_user_db, get_db
from app.models import UserTable, UserCreate, UserRead, UserUpdate
from app.routers import auth, users, contacts

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
SECRET = os.getenv("SECRET")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=None,
    get_strategy=get_jwt_strategy,
)

class UserManager(BaseUserManager[UserTable, int]):
    user_db_model = UserTable
    password_helper = PasswordHelper()

    async def on_after_register(self, user: UserTable, request=None):
        print(f"User {user.id} has registered.")

    async def create(self, user: UserCreate, safe: bool = False) -> UserTable:
        await self.validate_password(user.password)
        hashed_password = self.password_helper.hash(user.password)
        db_user = UserTable(
            email=user.email,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
        )
        try:
            async with self.user_db.session() as session:
                session.add(db_user)
                await session.commit()
                return db_user
        except IntegrityError:
            raise HTTPException(status_code=409, detail="User with this email already exists")

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[UserCreate, UserRead, UserUpdate](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()

origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

Base.metadata.create_all(bind=engine)
