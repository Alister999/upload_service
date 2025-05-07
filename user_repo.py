from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from models import UploadedFile

class FileRepository(SQLAlchemyAsyncRepository[UploadedFile]):
    model_type = UploadedFile