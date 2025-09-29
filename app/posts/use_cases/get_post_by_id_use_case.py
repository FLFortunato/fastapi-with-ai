from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.model.post import Post
from app.posts.repository.post_repository import PostRepository


class GetPostByIdUseCase:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.postRepo = PostRepository(db)

    async def execute(self, id: int) -> Post | None:
        try:
            result = await self.postRepo.getById(id)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id {id} not found.",
                )
            else:
                return result
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
