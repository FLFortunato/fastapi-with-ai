from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.use_cases.get_current_user_use_case import ValidateAuthentication
from app.db.session import get_db
from app.users.schemas.user import UserCreate, UserOutput
from app.users.use_cases.create_user import CreateUserUseCase
from app.users.use_cases.get_user_by_id import GetUseByIdUseCase

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(ValidateAuthentication.execute)],
)


@router.post("/")
async def createUser(user: UserCreate, db: AsyncSession = Depends(get_db)):
    use_case = CreateUserUseCase()
    return await use_case.execute(db, user)


@router.get("/{user_id}", response_model=UserOutput)
async def getUserById(user_id: int, db: AsyncSession = Depends(get_db)):
    use_case = GetUseByIdUseCase()
    return await use_case.execute(db, user_id)
