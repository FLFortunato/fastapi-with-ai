from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.repository.post_repository import PostRepository
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status


class DeletePostUseCase:

    @staticmethod
    async def execute(
        db: AsyncSession,
        id: int,
    ):
        try:
            result = await PostRepository.delete(db, id)
            if result == 0:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
                )

            await db.commit()

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )
