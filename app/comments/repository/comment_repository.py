from sqlalchemy.ext.asyncio import AsyncSession

from app.comments.model.comment import Comment
from app.comments.schema.comment_schema import CreateComment, UpdateComment
from app.utils.crud_factory import CrudFactory


class CommentRepository(CrudFactory[Comment, CreateComment, UpdateComment]):
    def __init__(self, db: AsyncSession):
        self.db = db
        super().__init__(db, Comment)
