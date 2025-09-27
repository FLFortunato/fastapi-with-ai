import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.db.session import Base, get_db  # sua função de dependência

DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"  # banco só em memória

# Criamos engine e session para os testes
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
AsyncSessionTest = async_sessionmaker(engine_test, expire_on_commit=False)


# Fixture do banco (setup/teardown)
@pytest.fixture(scope="function")
async def db_session():
    async with engine_test.begin() as conn:
        # cria tabelas antes do teste
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionTest() as session:
        yield session
    async with engine_test.begin() as conn:
        # dropa tabelas depois do teste (limpeza)
        await conn.run_sync(Base.metadata.drop_all)


# Fixture para sobrescrever get_db no FastAPI
@pytest.fixture(autouse=True)
def override_get_db(monkeypatch, db_session):
    async def _override():
        yield db_session

    monkeypatch.setattr("app.db.session.get_db", _override)
