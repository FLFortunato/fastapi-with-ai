import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model.user import User
from app.users.repository.user import UserRepository
from app.users.schemas.user import UserUpdate


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
async def test_update_user_success(db_session: AsyncSession):
    repo = UserRepository(db_session)

    user = await repo.get_by_id(1)
    if user is not None:
        result = await repo.update(user, UserUpdate(name="Test"))

        assert result.name == "Test" and result.id == 1
