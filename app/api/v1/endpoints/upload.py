from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.services.upload_service import upload_file
from app.schemas.file import ResponseFile

router = APIRouter()


@router.post("/upload", response_model=ResponseFile)
async def upload_file_endpoint(file: UploadFile = File(...),
                               db: AsyncSession = Depends(get_db)) -> ResponseFile:
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large"
        )
    result = await upload_file(file, db)
    return result