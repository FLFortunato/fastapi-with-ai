from app.comments.repository.comment_repository import CommentRepository
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


class DeleteCommentUseCase:

    @staticmethod
    async def execute(db: AsyncSession, id: int):
        try:
            logger.info(f"Trying to delete comment: {id}")
            result = await CommentRepository.delete(db, id)
            logger.info(f"Comment deletion result {result}")

            if result == 0:
                logger.warning(f"Comment with id {id} not found")
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Comment with id {id} not fould",
                )
            else:
                return result
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
