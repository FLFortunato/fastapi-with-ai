from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model.user import User
from app.users.schemas.user import UserCreate, UserUpdate


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserCreate) -> User:
        new_user = User(**user.model_dump())
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def getAll(self) -> list[User]:
        results = await self.db.execute(select(User))
        return list(results.scalars().all())

    async def get_by_id(self, id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def update(self, db_user: User, user_update: UserUpdate) -> User:
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete(self, db_user: User) -> None:
        await self.db.delete(db_user)
        await self.db.commit()
