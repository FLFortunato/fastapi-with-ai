from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.repository.user import UserRepository


class GetUseByIdUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.userRepo = UserRepository(db)

    async def execute(self, id: int):
        user = await self.userRepo.get_by_id(id)

        if not user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
            )
        return user
