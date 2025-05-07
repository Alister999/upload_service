import boto3
import hashlib
import uuid
import os
from fastapi import HTTPException, UploadFile as FastAPIUploadFile
from botocore.exceptions import ClientError

class MinIOService:
    def __init__(self, endpoint: str, access_key: str,
                 secret_key: str, bucket_name: str = "my-bucket"):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self._ensure_bucket()


    def _ensure_bucket(self) -> None:
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                try:
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                except ClientError as create_error:
                    raise HTTPException(status_code=500, detail=f"Failed to create bucket: {str(create_error)}")
            else:
                raise HTTPException(status_code=500, detail=f"Failed to check bucket: {str(e)}")


    async def upload_file(self, file: FastAPIUploadFile) -> tuple[str, str, str]:
        file_extension = os.path.splitext(file.filename)[1].lower()
        object_name = f"{uuid.uuid4()}{file_extension}"

        file_content = await file.read()
        sha256_hash = hashlib.sha256(file_content).hexdigest()

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file_content,
                ContentType=file.content_type,
            )
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload to MinIO: {str(e)}")

        file_url = f"{os.getenv('MINIO_ENDPOINT')}/{self.bucket_name}/{object_name}"

        return object_name, file_url, sha256_hash

    def delete_file(self, object_name: str) -> None:
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file from MinIO: {str(e)}")