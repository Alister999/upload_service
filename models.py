import uuid
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass

class UploadedFile(Base):
    __tablename__ = 'upload_file'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4)
    file_name: Mapped[str]
    hash: Mapped[str] = mapped_column(index=True, nullable=True, default=None)
    url: Mapped[str] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, unique=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    access_token: Mapped[str] = mapped_column(unique=True, nullable=True, default=None)
    refresh_token: Mapped[str] = mapped_column(unique=True, nullable=True, default=None)
