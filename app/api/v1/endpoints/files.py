import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.utils import get_current_user
from app.models.user import User
from app.schemas.file import ResponseFile, UpdateFile
from app.services.file_service import get_files_list, update_file, delete_file

router = APIRouter()


@router.get('/files', response_model=List[ResponseFile])
async def get_files(db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(get_current_user)) -> List[ResponseFile]:
    result = await get_files_list(db)
    return result


@router.put('/files/{file_id}', response_model=UpdateFile)
async def change_files(file_id: uuid.UUID,
                       data: UpdateFile,
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)) -> UpdateFile:
    result = await update_file(file_id, data, db)
    return result


@router.delete('/files/{file_id}', status_code=200)
async def delete_files(file_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(get_current_user)) -> dict:
    if await delete_file(file_id, db):
        return {"Response": f"File with ID {file_id} was deleted"}
    else:
        raise HTTPException(
            status_code=400,
            detail='Something went wrong'
        )
