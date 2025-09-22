from sqlalchemy.ext.asyncio import AsyncSession
from app.comments.model.comment import Comment
from app.comments.repository.comment_repository import CommentRepository
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

import logging

logger = logging.getLogger(__name__)


class GetCommentByIdUseCase:

    @staticmethod
    async def execute(db: AsyncSession, id: int) -> Comment | None:
        try:
            result = await CommentRepository.getById(db, id)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Comment with id: {id} not found",
                )
            return result
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
