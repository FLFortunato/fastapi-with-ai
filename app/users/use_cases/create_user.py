from fastapi import HTTPException
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.repository.user import UserRepository
from app.users.schemas.user import UserCreate
from app.utils.security import hash_password


class CreateUserUseCase:

    @staticmethod
    async def execute(db: AsyncSession, user_create: UserCreate):
        try:
            data: dict = user_create.model_dump()

            hashedPassword = await hash_password(data["password"])
            
            data["password"] = hashedPassword
            return await UserRepository.create(db, UserCreate(**data))
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Email already exists")
        except DataError as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
