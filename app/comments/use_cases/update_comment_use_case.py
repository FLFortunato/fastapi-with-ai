from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.comments.model.comment import Comment
from app.comments.repository.comment_repository import CommentRepository
from app.comments.schema.comment_schema import UpdateComment
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError


class UpdateCommentUseCase:

    @staticmethod
    async def execute(db: AsyncSession, id: int, comment: UpdateComment) -> Comment:
        try:
            result = await CommentRepository.update(db, id, comment)
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
