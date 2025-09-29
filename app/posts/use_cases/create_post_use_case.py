from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.model.post import Post
from app.posts.repository.post_repository import PostRepository
from app.posts.schema.post_schema import CreatePost


class CreatePostUseCase:
    def __init__(self, db: AsyncSession):
        self.postRepo = PostRepository(db)
        self.db = db

    async def execute(self, post: CreatePost) -> Post:
        try:
            result = await self.postRepo.create(post)
            return result
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error: {str(e)}",
            )
