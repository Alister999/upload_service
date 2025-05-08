import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
# from main import app, get_db, get_minio_service
# from db_config import db_config
# from minio_service import MinIOService
# from models import Base
import testing.postgresql
from advanced_alchemy.config import SQLAlchemyAsyncConfig
from contextlib import asynccontextmanager
from unittest.mock import Mock, AsyncMock

from app.core.database import get_db, db_config
from app.core.storage import MinIOService
from app.core.utils import get_minio_service
from app.main import app
from app.models.general import Base


@asynccontextmanager
async def test_lifespan(app: FastAPI):
    print("Using test_lifespan")
    yield


test_app = FastAPI(lifespan=test_lifespan)
test_app.include_router(app.router)


@pytest.fixture(scope="session")
def pg_tmp():
    with testing.postgresql.Postgresql() as pg:
        yield pg


@pytest_asyncio.fixture
async def test_engine(pg_tmp):
    TEST_DATABASE_URL = pg_tmp.url().replace("postgresql://", "postgresql+asyncpg://")
    print(f"Test DB URL: {TEST_DATABASE_URL}")
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
def test_db_config(pg_tmp):
    TEST_DATABASE_URL = pg_tmp.url().replace("postgresql://", "postgresql+asyncpg://")
    return SQLAlchemyAsyncConfig(connection_string=TEST_DATABASE_URL)


@pytest_asyncio.fixture
async def test_session(test_engine):
    TestAsyncSessionLocal = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with TestAsyncSessionLocal() as session:
        yield session


async def override_get_db(test_session: AsyncSession):
    yield test_session

def override_get_minio_service():
    minio_service = Mock(spec=MinIOService)
    minio_service.upload_file = AsyncMock(return_value=(None, "http://minio/test.pdf", "abc123"))
    minio_service.delete_file = AsyncMock(return_value=None)
    return minio_service

def override_db_config(test_db_config):
    return test_db_config

test_app.dependency_overrides[get_db] = lambda: override_get_db
test_app.dependency_overrides[get_minio_service] = override_get_minio_service
test_app.dependency_overrides[db_config] = override_db_config


@pytest_asyncio.fixture
async def client(test_db_config):
    async with test_db_config.get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    with TestClient(test_app, base_url="http://test") as c:
        yield c
    async with test_db_config.get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(autouse=True)
async def setup_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

