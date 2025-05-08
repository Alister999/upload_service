from sqlalchemy.orm import Mapped, mapped_column
from app.models.general import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, unique=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    access_token: Mapped[str] = mapped_column(unique=True, nullable=True, default=None)
    refresh_token: Mapped[str] = mapped_column(unique=True, nullable=True, default=None)
