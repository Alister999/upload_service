import os
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.file import UploadedFile
from app.schemas.file import ResponseFile
from app.core.database import FileRepository
from app.core.config import settings
from app.core.storage import MinIOService


async def upload_file(file: UploadFile, db: AsyncSession) -> ResponseFile:
    repo = FileRepository(session=db)

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=403,
            detail='Wrong extension'
        )

    if await repo.get_one_or_none(UploadedFile.file_name == file.filename):
        raise HTTPException(
            status_code=403,
            detail=f'File with name {file.filename} already exist'
        )

    minio_s = MinIOService()
    _, file_url, sha256_hash = await minio_s.upload_file(file)

    file_record = UploadedFile(
        file_name=file.filename,
        hash=sha256_hash,
        url=file_url,
    )

    await repo.add(file_record)
    await db.commit()
    await db.refresh(file_record)
    return ResponseFile.model_validate(file_record)