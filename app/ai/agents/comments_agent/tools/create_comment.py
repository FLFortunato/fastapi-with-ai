from app.comments.schema.comment_schema import CreateComment
from app.comments.use_cases.create_comment_use_case import CreateCommentUseCase
from app.db.session import get_db


async def handle_create_comment(user_id: int, post_id: int, content: str):
    """
    Tool used to create a new comment

    A new comment should only be created for a valid post.

    Fields required to create a comment:

    user_id: An integer that is the id of the user.
    post_id: An integer that is the id of the post.
    comment: string that is the comment
    """

    print("==================", user_id, post_id, content)

    if not user_id:
        return {"success": False, "message": "User id not provided"}

    if not post_id:
        return {"success": False, "message": "Post id not provided"}

    if len(content) < 10:
        return {"success": False, "message": "Content too short"}

    try:
        db_gen = get_db()
        db = await anext(db_gen)
        result = await CreateCommentUseCase(db).execute(
            CreateComment(content=content, user_id=user_id, post_id=post_id)
        )

        return {"success": True, "data": result}
    except Exception as e:
        # Aqui você pega QUALQUER erro (duplicado, db, etc) e trata
        return {"success": False, "message": str(e)}
