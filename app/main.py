from fastapi import FastAPI

from app.ai.controller import ai_controller
from app.auth.controller import auth_controller
from app.comments.controller import comment_controller
from app.posts.controller import post
from app.users.controller import users

app = FastAPI()


app.include_router(users.router)
app.include_router(comment_controller.router)
app.include_router(post.router)
app.include_router(auth_controller.router)
app.include_router(ai_controller.router)
