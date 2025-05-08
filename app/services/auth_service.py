import os
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db, UserRepository
from app.core.utils import verify_password, hash_password
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate, UserLogin, RefreshToken
from app.services.auth_utils import create_access_token, create_refresh_token


async def reg_user(user: UserCreate, db: AsyncSession) -> UserResponse:
    repo = UserRepository(session=db)

    if await repo.get_one_or_none(User.username == user.username):
        raise HTTPException(
            status_code=403,
            detail=f'User with username {User.username} not found'
        )

    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password)
    )
    await repo.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserResponse.model_validate(new_user)


async def login_user(user: UserLogin, db: AsyncSession) -> dict:
    repo = UserRepository(session=db)
    db_user = await repo.get_one_or_none(User.username == user.username)

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=403,
            detail='Invalid credentials'
        )

    access_token = create_access_token({"sub": db_user.username})
    refresh_token = create_refresh_token({"sub": db_user.username})

    db_user.access_token = access_token
    db_user.refresh_token = refresh_token

    await repo.update(db_user)
    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


async def refresh_my_token(data: RefreshToken, db: AsyncSession) -> dict:
    repo = UserRepository(session=db)

    try:
        payload = jwt.decode(data.refresh_token, os.getenv("SECRET_KEY"), algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=403,
                detail='Invalid credentials'
            )
        new_access_token = create_access_token({"sub": username})

        db_user = await repo.get_one_or_none(User.refresh_token == data.refresh_token)
        if not db_user:
            raise HTTPException(
                status_code=404,
                detail='User not found'
            )

        db_user.access_token = new_access_token
        await repo.update(db_user)
        await db.commit()

        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(
            status_code=403,
            detail='Invalid refresh token'
        )

