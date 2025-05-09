import uuid
from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.file import UploadedFile
from app.schemas.file import ResponseFile, UpdateFile
from app.core.database import FileRepository
from app.core.config import settings

from app.core.storage import MinIOService


async def get_files_list(db: AsyncSession) -> List[ResponseFile]:
    repo = FileRepository(session=db)
    get_files = await repo.list()
    return [ResponseFile.model_validate(file) for file in get_files]


async def update_file(file_id: uuid.UUID, data: UpdateFile,
                      db: AsyncSession) -> UpdateFile:
    repo = FileRepository(session=db)
    file = await repo.get_one_or_none(UploadedFile.id == file_id)
    if not file:
        raise HTTPException(
            status_code=404,
            detail= f'File with ID {file_id} not found'
        )

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key != 'id':
            setattr(file, key, value)

    await repo.update(file)
    await db.commit()
    await db.refresh(file)

    return UpdateFile.model_validate(file)



async def delete_file(
    file_id: uuid.UUID,
    db: AsyncSession
) -> bool:
    repo = FileRepository(session=db)
    file = await repo.get_one_or_none(UploadedFile.id == file_id)
    if not file:
        raise HTTPException(
            status_code=404,
            detail=f"File with ID {file_id} not found"
        )

    if file.url:
        try:
            prefix = f"{settings.MINIO_ENDPOINT}/my-bucket/"
            if not file.url.startswith(prefix):
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid file URL format: {file.url}"
                )
            object_name = f'{file.file_name}'
            minio_s = MinIOService()
            minio_s.delete_file(object_name)  # Синхронный вызов
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to delete file from MinIO: {str(e)}"
            )

    await repo.delete(file_id)
    await db.commit()
    return True