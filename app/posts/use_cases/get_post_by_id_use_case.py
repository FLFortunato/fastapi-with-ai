from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.posts.model.post import Post
from app.posts.repository.post_repository import PostRepository
from fastapi import HTTPException, status


class GetPostByIdUseCase:
    @staticmethod
    async def execute(db: AsyncSession, id: int) -> Post | None:
        try:
            result = await PostRepository.getById(db, id)

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
