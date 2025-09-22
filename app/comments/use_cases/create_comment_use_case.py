from sqlalchemy.ext.asyncio import AsyncSession
from app.comments.model.comment import Comment
from app.comments.repository.comment_repository import CommentRepository
from app.comments.schema.comment_schema import CreateComment
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


class CreateCommentUseCase:

    @staticmethod
    async def execute(db: AsyncSession, comment: CreateComment) -> Comment:
        try:
            result = await CommentRepository.create(db, comment)
            return result
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Comment already exists")
        except DataError as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
