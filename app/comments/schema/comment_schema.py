from pydantic import BaseModel
from typing import Optional


class CreateComment(BaseModel):
    title: str
    comment: str
    user_id: int
    post_id: int


class UpdateComment(BaseModel):
    title: Optional[str]
    comment: Optional[str]
    id: int


class CommentOut(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int

    class Config:
        orm_mode = True  # permite usar `.from_orm()` com SQLAlchemy
