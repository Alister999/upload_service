import os.path
from contextlib import asynccontextmanager
from typing import Optional, List

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db_config import init_db, db_config
from models import UploadedFile
from schemas import ResponseFile, CreateFile
from user_repo import UserRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("📦 Init DB...")
    await init_db()
    yield
    print("🧹 Shutdown...")


app = FastAPI(debug=True, lifespan=lifespan)

async def get_db() -> AsyncSession:
    async with db_config.get_session() as session:
        yield session


@app.post('/upload', response_model=ResponseFile)
async def upload(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)) -> ResponseFile:
    allowed_extentions = [".dcm", ".jpg", ".png", ".pdf"]
    file_extention = os.path.splitext(file.filename)[1].lower()
    if file_extention not in allowed_extentions:
        raise HTTPException(status_code=400, detail='Wrong extention')

    new_file = UploadedFile(file_name=file.filename)
    repo = UserRepository(session=db)
    await repo.add(new_file)
    await db.commit()
    await db.refresh(new_file)

    # return {
    #     "responce": "All is OK",
    #     "file_name": file.filename
    # }
    return ResponseFile.model_validate(new_file)


@app.get('/files', response_model=List[ResponseFile])
async def get_files(db: AsyncSession = Depends(get_db)) -> List[ResponseFile]:
    repo = UserRepository(session=db)
    files = await repo.list()
    ready_files = [ResponseFile.model_validate(file) for file in files]

    # return {
    #     "responce": "Get is OK"
    # }
    return ready_files


