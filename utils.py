import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, FastAPI
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from db_config import db_config, init_db
from minio_service import MinIOService
# from config import ALGORITHM # SECRET_KEY,
# from database import session_local
from models import User
from user_repo import UserRepository

load_dotenv()

ALGORITHM = os.getenv('ALGORITHM')

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Init DB...")
    await init_db()
    yield
    print("Shutdown...")


async def get_db() -> AsyncSession:
    async with db_config.get_session() as session:
        yield session


def get_minio_service() -> MinIOService:
    return MinIOService(
        endpoint=os.getenv('MINIO_ENDPOINT'),
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        bucket_name="my-bucket",
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    repo = UserRepository(session=db)
    user = await repo.get_one_or_none(User.username == username)

    if user is None:
        raise credentials_exception
    return user