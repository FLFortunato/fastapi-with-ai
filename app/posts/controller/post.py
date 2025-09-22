from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.session import get_db
from app.posts.model.post import Post
from app.posts.schema.post_schema import CreatePost, OutputPost, UpdatePost
from app.posts.use_cases.create_post_use_case import CreatePostUseCase
from app.posts.use_cases.delete_post_use_case import DeletePostUseCase
from app.posts.use_cases.get_all_posts_use_case import GetAllPostsUseCase
from app.posts.use_cases.update_post_use_case import UpdatePostUseCase


router = APIRouter(prefix="posts", tags=["Posts"])


@router.get("/")
async def getAllPosts(db: AsyncSession = Depends(get_db)):
    use_case = GetAllPostsUseCase()
    return await use_case.execute(db)

@router.get('/{post_id}')
async def getPostById(db:AsyncSession, id:int) -> Post | None:
    use_case = 

@router.post("/", response_model=OutputPost)
async def createPost(db: AsyncSession, post: CreatePost) -> Post:
    use_case = CreatePostUseCase()
    return await use_case.execute(db, post)


@router.put("/{post_id}")
async def updatePost(db: AsyncSession, post: UpdatePost, post_id: int):
    use_case = UpdatePostUseCase()
    return await use_case.execute(db, post, post_id)


@router.delete("/{post_id}")
async def deletePost(db: AsyncSession, id: int) -> None:
    use_case = DeletePostUseCase()
    return await use_case.execute(db, id)
