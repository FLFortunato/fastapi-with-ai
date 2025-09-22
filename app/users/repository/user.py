from sqlalchemy.ext.asyncio import AsyncSession
from app.users.model.user import User
from sqlalchemy import select

from app.users.schemas.user import UserCreate, UserUpdate


class UserRepository:
    @staticmethod
    async def create(db: AsyncSession, user: UserCreate) -> User:
        new_user = User(**user.model_dump())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def getAll(db: AsyncSession) -> list[User]:
        results = await db.execute(select(User))
        return list(results.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, id: int) -> User | None:
        result = await db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, db_user: User, user_update: UserUpdate) -> User:
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def delete(db: AsyncSession, db_user: User) -> None:
        await db.delete(db_user)
        await db.commit()
