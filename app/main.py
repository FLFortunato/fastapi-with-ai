from fastapi import FastAPI
from app.users.controller import users
from app.comments.controller import comment_controller
from app.posts.controller import post

app = FastAPI()


app.include_router(users.router)
app.include_router(comment_controller.router)
app.include_router(post.router)
