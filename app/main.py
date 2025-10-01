from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ai.controller import ai_controller
from app.auth.controller import auth_controller
from app.comments.controller import comment_controller
from app.posts.controller import post
from app.users.controller import users

app = FastAPI()


# Configuração de CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # permite apenas esses domínios
    allow_credentials=True,
    allow_methods=["*"],  # permite GET, POST, etc.
    allow_headers=["*"],  # permite todos os headers
)


app.include_router(users.router)
app.include_router(comment_controller.router)
app.include_router(post.router)
app.include_router(auth_controller.router)
app.include_router(ai_controller.router)
