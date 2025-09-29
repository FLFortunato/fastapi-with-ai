import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model.user import User
from app.users.repository.user import UserRepository
from app.users.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_get_all_users(db_session: AsyncSession):
    user1 = User(
        email="a@test.com", name="Alice", lastName="Test", password="123", role="dev"
    )
    user2 = User(
        email="b@test.com", name="Bob", lastName="Test", password="456", role="dev"
    )

    db_session.add_all([user1, user2])
    await db_session.commit()

    repo = UserRepository(db_session)
    users = await repo.getAll()

    assert len(users) == 2
    assert users[0].email == "a@test.com"
