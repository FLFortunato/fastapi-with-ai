from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.model.post import Post
from app.posts.schema.post_schema import CreatePost, UpdatePost
from app.utils.crud_factory import CrudFactory


class PostRepository(CrudFactory[Post, CreatePost, UpdatePost]):
    def __init__(self, db: AsyncSession):
        self.db = db
        super().__init__(db, Post)
