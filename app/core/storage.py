from io import BytesIO
from minio import Minio
from minio.error import S3Error
from app.core.config import settings
import logging
import hashlib
from fastapi import UploadFile

logger = logging.getLogger(__name__)

class MinIOService:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=settings.MINIO_SECURE
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self._ensure_bucket()

    def _ensure_bucket(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Bucket {self.bucket_name} created")
            else:
                logger.info(f"Bucket {self.bucket_name} already exists")
        except S3Error as e:
            logger.error(f"Error ensuring bucket {self.bucket_name}: {e}")
            raise

    async def upload_file(self, file: UploadFile) -> tuple[str, str, str]:
        try:
            file_data = await file.read()
            hash_value = hashlib.sha256(file_data).hexdigest()
            self.client.put_object(
                self.bucket_name,
                file.filename,
                data=BytesIO(file_data),
                length=len(file_data)
            )
            url = f"{settings.MINIO_EXTERNAL_ENDPOINT}/{self.bucket_name}/{file.filename}"
            logger.info(f"File {file.filename} uploaded to {url}")
            return None, url, hash_value
        except S3Error as e:
            logger.error(f"Error uploading file {file.filename}: {e}")
            raise

    def delete_file(self, file_name: str):
        try:
            self.client.remove_object(self.bucket_name, file_name)
            logger.info(f"File {file_name} deleted from bucket {self.bucket_name}")
        except S3Error as e:
            logger.error(f"Error deleting file {file_name}: {e}")
            raise