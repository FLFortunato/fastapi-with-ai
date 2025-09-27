from typing import List

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.model.post import Post
from app.posts.schema.post_schema import CreatePost, UpdatePost


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, create_post: CreatePost) -> Post:
        post = Post(**create_post.model_dump())
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def getAll(self) -> List[Post]:
        results = await self.db.execute(select(Post))
        return list(results.scalars().all())

    async def getById(self, id: int) -> Post | None:
        result = await self.db.execute(select(Post).where(Post.id == id))
        return result.scalar_one_or_none()

    async def update(self, id: int, post: UpdatePost) -> Post | None:
        stmt = (
            update(Post)
            .where(Post.id == id)
            .values(**post.model_dump())
            .returning(Post)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete(self, id: int) -> int:
        stmt = delete(Post).where(Post.id == id)
        result = await self.db.execute(stmt)

        return result.rowcount
