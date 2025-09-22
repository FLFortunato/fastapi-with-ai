from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import List
from app.comments.model.comment import Comment
from app.comments.schema.comment_schema import CommentOut, CreateComment, UpdateComment
from app.comments.use_cases.create_comment_use_case import CreateCommentUseCase
from app.comments.use_cases.delete_comment_use_case import DeleteCommentUseCase
from app.comments.use_cases.get_all_comments_use_case import GetAllCommentsUseCase
from app.comments.use_cases.get_comment_by_id import GetCommentByIdUseCase
from app.comments.use_cases.update_comment_use_case import UpdateCommentUseCase
from app.db.session import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=List[CommentOut])
async def getAllComments(db: AsyncSession = Depends(get_db)):
    use_case = GetAllCommentsUseCase()
    return await use_case.execute(db)


@router.get("/{id}", response_model=CommentOut)
async def getCommentById(id: int, db: AsyncSession = Depends(get_db)):
    use_case = GetCommentByIdUseCase()
    return await use_case.execute(db, id)


@router.post("/", response_model=CommentOut)
async def createComment(comment: CreateComment, db: AsyncSession = Depends(get_db)):
    use_case = CreateCommentUseCase()
    return await use_case.execute(db, comment)


@router.put("/{id}", response_model=CommentOut)
async def updateComment(
    id: int, comment: UpdateComment, db: AsyncSession = Depends(get_db)
):
    use_case = UpdateCommentUseCase()
    return await use_case.execute(db, id, comment)


@router.delete("/{id}")
async def deleteComment(id: int, db: AsyncSession = Depends(get_db)):
    use_case = DeleteCommentUseCase()
    return await use_case.execute(db, id)
