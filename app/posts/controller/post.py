from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.posts.model.post import Post
from app.posts.schema.post_schema import CreatePost, OutputPost, UpdatePost
from app.posts.use_cases.create_post_use_case import CreatePostUseCase
from app.posts.use_cases.delete_post_use_case import DeletePostUseCase
from app.posts.use_cases.get_all_posts_use_case import GetAllPostsUseCase
from app.posts.use_cases.get_many_posts_use_case import get_many_posts_use_case
from app.posts.use_cases.get_post_by_id_use_case import GetPostByIdUseCase
from app.posts.use_cases.update_post_use_case import UpdatePostUseCase

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/")
async def getAllPosts(db: AsyncSession = Depends(get_db)):
    use_case = GetAllPostsUseCase(db)
    return await use_case.execute()


@router.get("/{post_id}")
async def getPostById(id: int, db: AsyncSession = Depends(get_db)):
    use_case = GetPostByIdUseCase(db)
    return await use_case.execute(id)


@router.post("/", response_model=OutputPost)
async def createPost(post: CreatePost, db: AsyncSession = Depends(get_db)):
    use_case = CreatePostUseCase(db)
    return await use_case.execute(post)


@router.put("/{post_id}")
async def updatePost(
    post: UpdatePost, post_id: int, db: AsyncSession = Depends(get_db)
):
    use_case = UpdatePostUseCase(db)
    return await use_case.execute(post, post_id)


@router.delete("/{post_id}")
async def deletePost(id: int, db: AsyncSession = Depends(get_db)) -> None:
    use_case = DeletePostUseCase(db)
    return await use_case.execute(id)


@router.get("/many/posts")
async def getManyPosts():

    return await get_many_posts_use_case()
