import os.path
import uuid
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db_config import init_db, db_config
from minio_service import MinIOService
from models import UploadedFile
from schemas import ResponseFile, UpdateFile
from user_repo import FileRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Init DB...")
    await init_db()
    yield
    print("Shutdown...")


app = FastAPI(debug=True, lifespan=lifespan)

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


@app.post('/upload', response_model=ResponseFile)
async def upload(file: UploadFile = File(...),
                 db: AsyncSession = Depends(get_db),
                 minio_service: MinIOService = Depends(get_minio_service),
                 ) -> ResponseFile:
    allowed_extentions = [".dcm", ".jpg", ".png", ".pdf"]
    file_extention = os.path.splitext(file.filename)[1].lower()
    if file_extention not in allowed_extentions:
        raise HTTPException(status_code=400, detail='Wrong extention')

    _, file_url, sha256_hash = await minio_service.upload_file(file)

    new_file = UploadedFile(
        file_name=file.filename,
        hash=sha256_hash,
        url=file_url,
    )

    repo = FileRepository(session=db)
    await repo.add(new_file)
    await db.commit()
    await db.refresh(new_file)

    return ResponseFile.model_validate(new_file)


@app.get('/files', response_model=List[ResponseFile])
async def get_files(db: AsyncSession = Depends(get_db)) -> List[ResponseFile]:
    repo = FileRepository(session=db)
    files = await repo.list()
    ready_files = [ResponseFile.model_validate(file) for file in files]

    return ready_files


@app.put('/files/{file_id: uuid.UUID}', response_model=UpdateFile)
async def change_files(file_id: uuid.UUID,
                       data: UpdateFile,
                       db: AsyncSession = Depends(get_db)) -> UpdateFile:
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


@app.delete('/files/{file_id: uuid.UUID}', status_code=200)
async def delete_files(file_id: uuid.UUID,
                       db: AsyncSession = Depends(get_db),
                       minio_service: MinIOService = Depends(get_minio_service),) -> dict:
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




