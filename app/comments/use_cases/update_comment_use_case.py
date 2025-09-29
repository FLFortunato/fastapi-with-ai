from fastapi import HTTPException, status
from sqlalchemy.exc import DataError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.comments.model.comment import Comment
from app.comments.repository.comment_repository import CommentRepository
from app.comments.schema.comment_schema import UpdateComment


class UpdateCommentUseCase:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.commentRepo = CommentRepository(db)

    async def execute(self, id: int, comment: UpdateComment) -> Comment | None:
        try:
            result = await self.commentRepo.update(id, comment)
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
