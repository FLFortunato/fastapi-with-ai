from pydantic import BaseModel
from typing import List
from app.comments.schema.comment_schema import CommentOut
from app.users.schemas.user import UserOutput


class CreatePost(BaseModel):
    title: str
    content: str
    user_id: int


class OutputPost(BaseModel):
    content: str
    user: UserOutput
    comments: List[CommentOut]

    class Config:
        orm_mode = True


class UpdatePost(BaseModel):
    title: str
    content: str
