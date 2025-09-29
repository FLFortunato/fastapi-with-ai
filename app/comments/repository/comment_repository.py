from typing import List

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.comments.model.comment import Comment
from app.comments.schema.comment_schema import CreateComment, UpdateComment


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, comment: CreateComment) -> Comment:
        new_comment = Comment(**comment.model_dump())
        self.db.add(new_comment)
        await self.db.commit()
        await self.db.refresh(new_comment)
        return new_comment

    async def getAll(self) -> List[Comment]:
        results = await self.db.execute(select(Comment))
        return list(results.scalars().all())

    async def getById(self, id: int) -> Comment | None:
        results = await self.db.execute(select(Comment).where(Comment.id == id))
        return results.scalar_one_or_none()

    async def update(self, id: int, comment: UpdateComment) -> Comment | None:
        stmt = (
            update(Comment)
            .where(Comment.id == id)
            .values(**comment.model_dump())
            .returning(Comment)
        )
        result = await self.db.execute(statement=stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete(self, id: int) -> int:
        stmt = delete(Comment).where(Comment.id == id)
        result = await self.db.execute(stmt)
        return result.rowcount
