import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import DataError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.comments.model.comment import Comment
from app.comments.repository.comment_repository import CommentRepository

logger = logging.getLogger(__name__)


class GetAllCommentsUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.commentRepo = CommentRepository(db)

    async def execute(self) -> List[Comment]:
        try:
            results = await self.commentRepo.getAll()
            return results
        except DataError as e:
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        except SQLAlchemyError as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
