from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.model.post import Post
from app.posts.repository.post_repository import PostRepository


class GetAllPostsUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.postRepo = PostRepository(db)

    async def execute(self) -> List[Post]:
        try:
            results = await self.postRepo.getAll()
            return results
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )
