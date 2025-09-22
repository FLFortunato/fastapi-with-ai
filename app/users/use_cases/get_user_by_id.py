from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.repository.user import UserRepository


class GetUseByIdUseCase:

    @staticmethod
    async def execute(db: AsyncSession, id: int):
        user = await UserRepository.get_by_id(db, id)

        if not user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
            )
        return user
