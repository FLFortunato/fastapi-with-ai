from fastapi import HTTPException
from sqlalchemy.exc import DataError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.comments.model.comment import Comment
from app.comments.repository.comment_repository import CommentRepository
from app.comments.schema.comment_schema import CreateComment


class CreateCommentUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.commentRepo = CommentRepository(db)

    async def execute(self, comment: CreateComment) -> Comment:
        try:
            result = await self.commentRepo.create(comment)
            return result
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Comment already exists")
        except DataError as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
