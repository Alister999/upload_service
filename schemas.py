import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseFile(BaseModel):
    class Config:
        from_attributes = True


class UpdateFile(BaseFile):
    id: Optional[uuid.UUID]
    hash: Optional[str]
    file_name: Optional[str]
    url: Optional[str]


class ResponseFile(BaseFile):
    id: uuid.UUID
    hash: Optional[str]
    file_name: str
    url: Optional[str]
    created_at: datetime

