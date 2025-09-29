from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model.user import User
from app.users.schemas.user import UserCreate, UserUpdate
from app.utils.crud_factory import CrudFactory


class UserRepository(CrudFactory[User, UserCreate, UserUpdate]):

    def __init__(self, db: AsyncSession):
        self.db = db
        super().__init__(db, User)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
