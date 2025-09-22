from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.posts.model.post import Post
from app.posts.repository.post_repository import PostRepository
from sqlalchemy.exc import SQLAlchemyError


class GetAllPostsUseCase:

    @staticmethod
    async def execute(db: AsyncSession) -> List[Post]:
        try:
            results = await PostRepository.getAll(db)
            return results
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )
