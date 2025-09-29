import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.comments.model.comment import Comment
from app.db.session import Base
from app.posts.model.post import Post
from app.users.model.user import User

DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"  # banco só em memória

# Criamos engine e session para os testes
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
AsyncSessionTest = async_sessionmaker(engine_test, expire_on_commit=False)


# Fixture do banco (setup/teardown)
@pytest_asyncio.fixture
async def db_session():
    async with engine_test.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        async with AsyncSessionTest(bind=conn) as session:
            yield session
        await conn.run_sync(Base.metadata.drop_all)


# Fixture para sobrescrever get_db no FastAPI
@pytest.fixture(autouse=True)
def override_get_db(monkeypatch, db_session):
    async def _override():
        yield db_session

    monkeypatch.setattr("app.db.session.get_db", _override)
