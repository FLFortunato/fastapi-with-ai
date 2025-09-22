from app.posts.repository.post_repository import PostRepository
from app.posts.schema.post_schema import UpdatePost
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError
from fastapi import HTTPException, status


class UpdatePostUseCase:

    @staticmethod
    async def execute(db: AsyncSession, post: UpdatePost, id: int):
        try:
            result = await PostRepository.update(db, id, post)
            return result
        except IntegrityError:
            raise HTTPException(
                status_code=400, detail="Integrity constraint violation"
            )
        except DataError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}",
            )
