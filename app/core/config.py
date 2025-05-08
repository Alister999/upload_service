from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50 MB
    ALLOWED_EXTENSIONS: List[str] = [".dcm", ".jpg", ".png", ".pdf"]
    MINIO_ENDPOINT: str = "http://minio:9000"
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    ALGORITHM: str #= "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int #= 15
    REFRESH_TOKEN_EXPIRE_DAYS: int #= 7
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"

settings = Settings()