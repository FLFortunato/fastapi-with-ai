from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema.token import RefreshRequest, Token
from app.auth.use_cases.login_use_case import LoginUseCase
from app.auth.use_cases.refresh_token_use_case import RefreshTokenUseCase
from app.db.session import get_db
from app.users.schemas.user import UserCreate, UserOutput
from app.users.use_cases.create_user import CreateUserUseCase

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOutput)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    use_case = CreateUserUseCase(db)
    return await use_case.execute(user_create=user)


@router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    return await LoginUseCase.execute(form, db)


@router.post("/refresh", response_model=Token)
async def refresh(refresh_token: RefreshRequest):
    return RefreshTokenUseCase.execute(refresh_token=refresh_token.refresh_token)
