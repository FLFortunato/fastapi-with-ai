from sqlalchemy.ext.asyncio import AsyncSession
from app.comments.model.comment import Comment
from typing import List
from sqlalchemy.exc import DataError
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.comments.repository.comment_repository import CommentRepository
import logging

logger = logging.getLogger(__name__)


class GetAllCommentsUseCase:

    @staticmethod
    async def execute(db: AsyncSession) -> List[Comment]:
        try:
            results = await CommentRepository.getAll(db)
            return results
        except DataError as e:
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        except SQLAlchemyError as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
