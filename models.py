import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass

class UploadFile(Base):
    __tablename__ = 'upload_file'

    UUID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, unique=True)
    hash: Mapped[str] = mapped_column(index=True)
    url: Mapped[str]
