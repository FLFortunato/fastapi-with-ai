from fastapi import HTTPException, status
from sqlalchemy.exc import DataError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.repository.post_repository import PostRepository
from app.posts.schema.post_schema import UpdatePost


class UpdatePostUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.postRepo = PostRepository(db)

    async def execute(self, post: UpdatePost, id: int):
        try:
            result = await self.postRepo.update(id, post)
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
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}",
            )
