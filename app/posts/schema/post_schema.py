from pydantic import BaseModel, EmailStr
from typing import Optional, List

from app.comments.model.comment import Comment
from app.users.model.user import User


class CreatePost(BaseModel):
    title: str
    content: str
    user_id: int


class OutputPost(BaseModel):
    content: str
    user: User
    comments: List[Comment]


class UpdatePost(BaseModel):
    title: str
    content: str
