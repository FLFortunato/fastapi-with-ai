from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.users.model.user import User
from app.users.repository.user import UserRepository


class GetUserByEmailUseCase:
    @staticmethod
    async def execute(email: str, db: AsyncSession) -> User:
        try:
            user = await UserRepository.get_by_email(db, email)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User not found for email: {email}",
                )
            else:
                return user
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
