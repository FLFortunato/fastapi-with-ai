from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.use_cases.get_current_user_use_case import ValidateAuthentication
from app.comments.schema.comment_schema import CommentOut, CreateComment, UpdateComment
from app.comments.use_cases.create_comment_use_case import CreateCommentUseCase
from app.comments.use_cases.delete_comment_use_case import DeleteCommentUseCase
from app.comments.use_cases.get_all_comments_use_case import GetAllCommentsUseCase
from app.comments.use_cases.get_comment_by_id import GetCommentByIdUseCase
from app.comments.use_cases.update_comment_use_case import UpdateCommentUseCase
from app.db.session import get_db

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
    # dependencies=[Depends(ValidateAuthentication.execute)],
)


@router.get("/", response_model=List[CommentOut])
async def getAllComments(db: AsyncSession = Depends(get_db)):
    use_case = GetAllCommentsUseCase(db)
    return await use_case.execute()


@router.get("/{id}", response_model=CommentOut)
async def getCommentById(id: int, db: AsyncSession = Depends(get_db)):
    use_case = GetCommentByIdUseCase(db)
    return await use_case.execute(id)


@router.post("/", response_model=CommentOut)
async def createComment(comment: CreateComment, db: AsyncSession = Depends(get_db)):
    use_case = CreateCommentUseCase(db)
    return await use_case.execute(comment)


@router.put("/{id}", response_model=CommentOut)
async def updateComment(
    id: int, comment: UpdateComment, db: AsyncSession = Depends(get_db)
):
    use_case = UpdateCommentUseCase(db)
    return await use_case.execute(id, comment)


@router.delete("/{id}")
async def deleteComment(id: int, db: AsyncSession = Depends(get_db)):
    use_case = DeleteCommentUseCase(db)
    return await use_case.execute(id)
