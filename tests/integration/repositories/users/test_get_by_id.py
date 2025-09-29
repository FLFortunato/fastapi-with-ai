import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model.user import User
from app.users.repository.user import UserRepository


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession):
    user = User(
        email="test@test.com.br",
        lastName="Fort",
        name="Filipi",
        password="12342",
        role="developer",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_get_by_id_success(db_session: AsyncSession, test_user):

    repo = UserRepository(db_session)

    result = await repo.get_by_id(1)

    assert result is not None and result.id is not None and result.id == 1


@pytest.mark.asyncio
async def test_get_by_id_failure(db_session: AsyncSession, test_user):

    repo = UserRepository(db_session)

    result = await repo.get_by_id(10)

    assert result is None
