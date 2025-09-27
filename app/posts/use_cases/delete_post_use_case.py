from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.repository.post_repository import PostRepository


class DeletePostUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.postRepo = PostRepository(db)

    async def execute(
        self,
        id: int,
    ):
        try:
            result = await self.postRepo.delete(id)
            if result == 0:
                await self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
                )

            await self.db.commit()

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )
