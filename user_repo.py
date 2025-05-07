from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from models import UploadedFile, User


class FileRepository(SQLAlchemyAsyncRepository[UploadedFile]):
    model_type = UploadedFile

class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User