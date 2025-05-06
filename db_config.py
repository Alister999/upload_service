import os

from advanced_alchemy.config import SQLAlchemyAsyncConfig
from dotenv import load_dotenv

from models import Base

load_dotenv()


database_url = f'postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:5432/{os.getenv("DB_NAME")}'
if not database_url:
    raise ValueError("DATABASE_URL is not set in .env file")

db_config = SQLAlchemyAsyncConfig(connection_string=database_url)

async def init_db():
    async with db_config.get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)