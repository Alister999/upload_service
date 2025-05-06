from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from models import UploadedFile

class UserRepository(SQLAlchemyAsyncRepository[UploadedFile]):
    model_type = UploadedFile