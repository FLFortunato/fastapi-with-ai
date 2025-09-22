from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List
from app.posts.model.post import Post
from app.posts.schema.post_schema import CreatePost, UpdatePost


class PostRepository:

    @staticmethod
    async def create(db: AsyncSession, create_post: CreatePost) -> Post:
        post = Post(**create_post.model_dump())
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def getAll(db: AsyncSession) -> List[Post]:
        results = await db.execute(select(Post))
        return list(results.scalars().all())

    @staticmethod
    async def getById(db: AsyncSession, id: int) -> Post | None:
        result = await db.execute(select(Post).where(Post.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, id: int, post: UpdatePost) -> Post | None:
        stmt = (
            update(Post)
            .where(Post.id == id)
            .values(**post.model_dump())
            .returning(Post)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none()

    @staticmethod
    async def delete(db: AsyncSession, id: int) -> int:
        stmt = delete(Post).where(Post.id == id)
        result = await db.execute(stmt)

        return result.rowcount
