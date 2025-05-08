import os.path
import uuid
from contextlib import asynccontextmanager
from typing import List

from advanced_alchemy.utils.sync_tools import await_
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.params import Depends
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from auth import create_access_token, create_refresh_token
from db_config import init_db, db_config
from minio_service import MinIOService
from models import UploadedFile, User
from schemas import ResponseFile, UpdateFile, UserCreate, UserResponse, UserLogin, RefreshToken
from user_repo import FileRepository, UserRepository
from utils import lifespan, get_db, get_minio_service, hash_password, verify_password, get_current_user


# app = FastAPI(debug=True, lifespan=lifespan)
app = FastAPI()
load_dotenv()
ALGORITHM = os.getenv('ALGORITHM')
MAX_FILE_SIZE = 50 * 1024 * 1024  # 52,428,800 byte


@app.post('/upload', response_model=ResponseFile)
async def upload(file: UploadFile = File(...),
                 db: AsyncSession = Depends(get_db),
                 minio_service: MinIOService = Depends(get_minio_service),
                 current_user: User = Depends(get_current_user),) -> ResponseFile:
    if file.size is None or file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=403,
            detail=f"File size exceeds limit of {MAX_FILE_SIZE // (1024 * 1024)} MB"
        )

    repo = FileRepository(session=db)

    allowed_extentions = [".dcm", ".jpg", ".png", ".pdf"]
    file_extention = os.path.splitext(file.filename)[1].lower()
    if file_extention not in allowed_extentions:
        raise HTTPException(status_code=400, detail='Wrong extention')

    if await repo.get_one_or_none(UploadedFile.file_name == file.filename):
        raise HTTPException(status_code=403, detail= f'File with name {file.filename} already exist')

    _, file_url, sha256_hash = await minio_service.upload_file(file)

    new_file = UploadedFile(
        file_name=file.filename,
        hash=sha256_hash,
        url=file_url,
    )

    await repo.add(new_file)
    await db.commit()
    await db.refresh(new_file)

    return ResponseFile.model_validate(new_file)


@app.get('/files', response_model=List[ResponseFile])
async def get_files(db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(get_current_user),) -> List[ResponseFile]:
    repo = FileRepository(session=db)
    files = await repo.list()
    ready_files = [ResponseFile.model_validate(file) for file in files]

    return ready_files


@app.put('/files/{file_id}', response_model=UpdateFile)
async def change_files(file_id: uuid.UUID,
                       data: UpdateFile,
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user),) -> UpdateFile:
    repo = FileRepository(session=db)
    file = await repo.get_one_or_none(UploadedFile.id == file_id)
    if not file:
        raise HTTPException(status_code=404, detail=f'File with ID {file_id} not found')

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key != 'id':
            setattr(file, key, value)

    await repo.update(file)
    await db.commit()
    await db.refresh(file)

    return UpdateFile.model_validate(file)


@app.delete('/files/{file_id}', status_code=200)
async def delete_files(file_id: uuid.UUID,
                       db: AsyncSession = Depends(get_db),
                       minio_service: MinIOService = Depends(get_minio_service),
                       current_user: User = Depends(get_current_user),) -> dict:
    repo = FileRepository(session=db)
    file = await repo.get_one_or_none(UploadedFile.id == file_id)
    if not file:
        raise HTTPException(status_code=404, detail=f'File with ID {file_id} not found')

    if file.url:
        try:
            object_name = file.url.split(f"{os.getenv('MINIO_ENDPOINT')}/my-bucket/")[-1]
            minio_service.delete_file(object_name)
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file from MinIO: {str(e)}")

    await repo.delete(file_id)
    await db.commit()

    return {"Response": f"File with ID {file_id} was deleted"}





@app.post('/register', response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    repo = UserRepository(session=db)

    if await repo.get_one_or_none(User.username == user.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password)
    )
    await repo.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserResponse.model_validate(new_user)


@app.post('/login')
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(session=db)

    db_user = await repo.get_one_or_none(User.username == user.username)

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

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


@app.post('/refresh')
async def refresh_token(data: RefreshToken, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(session=db)

    try:
        payload = jwt.decode(data.refresh_token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        new_access_token = create_access_token({"sub": username})

        db_user = await repo.get_one_or_none(User.refresh_token == data.refresh_token)
        if not db_user:
            raise HTTPException(status_code=404, detail='User not found')

        db_user.access_token = new_access_token
        await repo.update(db_user)
        await db.commit()

        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
