from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.model.post import Post
from app.posts.repository.post_repository import PostRepository
from app.posts.schema.post_schema import CreatePost
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status


class CreatePostUseCase:

    @staticmethod
    async def execute(db: AsyncSession, post: CreatePost) -> Post:
        try:
            result = await PostRepository.create(db, post)
            return result
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error: {str(e)}",
            )
