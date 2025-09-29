import logging
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.repository.user import UserRepository
from app.users.schemas.user import UserCreate

logging.basicConfig(level=logging.INFO)


@pytest.mark.asyncio
async def test_create_user_success(db_session: AsyncSession):

    repo = UserRepository(db_session)
    user_to_create = UserCreate(
        email="test@test.com.br",
        name="Jhon",
        lastName="test",
        password="243232",
        role="developer",
    )

    new_user = await repo.create(user_to_create)

    assert new_user.id == 1


@pytest.mark.asyncio
async def test_create_user_fail(db_session: AsyncSession):
    with pytest.raises(ValidationError):
        repo = UserRepository(db_session)
        user_to_create = UserCreate(
            email="testtest.com.br",
            name="Jhon",
            lastName="test",
            password="243232",
            role="developer",
        )

        await repo.create(user_to_create)
