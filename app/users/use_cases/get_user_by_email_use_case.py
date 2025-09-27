from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model.user import User
from app.users.repository.user import UserRepository


class GetUserByEmailUseCase:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.userRepo = UserRepository(db)

    async def execute(self, email: str) -> User:
        try:
            user = await self.userRepo.get_by_email(email)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User not found for email: {email}",
                )
            else:
                return user
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
