from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserResponse, UserCreate, UserLogin, RefreshToken
from app.services.auth_service import reg_user, login_user, refresh_my_token

router = APIRouter()


@router.post('/register', response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    result = await reg_user(user, db)
    return result


@router.post('/login')
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)) -> dict:
    result = await login_user(user, db)
    return result


@router.post('/refresh')
async def refresh_token(data: RefreshToken, db: AsyncSession = Depends(get_db)) -> dict:
    result = await refresh_my_token(data, db)
    return result