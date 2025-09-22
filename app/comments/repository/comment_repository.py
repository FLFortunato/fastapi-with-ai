from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.comments.schema.comment_schema import CreateComment, UpdateComment
from app.comments.model.comment import Comment
from typing import List


class CommentRepository:

    @staticmethod
    async def create(db: AsyncSession, comment: CreateComment) -> Comment:
        new_comment = Comment(**comment.model_dump())
        db.add(new_comment)
        await db.commit()
        await db.refresh(new_comment)
        return new_comment

    @staticmethod
    async def getAll(db: AsyncSession) -> List[Comment]:
        results = await db.execute(select(Comment))
        return list(results.scalars().all())

    @staticmethod
    async def getById(db: AsyncSession, id: int) -> Comment | None:
        results = await db.execute(select(Comment).where(Comment.id == id))
        return results.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, id: int, comment: UpdateComment) -> Comment:
        stmt = (
            update(Comment)
            .where(Comment.id == id)
            .values(**comment.model_dump())
            .returning(Comment)
        )
        result = await db.execute(statement=stmt)
        await db.commit()
        return result.scalar_one_or_none()

    @staticmethod
    async def delete(db: AsyncSession, id: int) -> int:
        stmt = delete(Comment).where(Comment.id == id)
        result = await db.execute(stmt)
        return result.rowcount
