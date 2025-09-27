from fastapi import HTTPException
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.repository.user import UserRepository
from app.users.schemas.user import UserCreate
from app.utils.security import hash_password


class CreateUserUseCase:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.userRepo = UserRepository(db)

    async def execute(self, user_create: UserCreate):
        try:
            data: dict = user_create.model_dump()

            hashedPassword = await hash_password(data["password"])

            data["password"] = hashedPassword
            return await self.userRepo.create(UserCreate(**data))
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Email already exists")
        except DataError as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
