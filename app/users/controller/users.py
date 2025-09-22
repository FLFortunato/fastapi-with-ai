from fastapi import APIRouter
from app.users.schemas.user import UserCreate
from app.users.use_cases.create_user import CreateUserUseCase
from app.users.use_cases.get_user_by_id import GetUseByIdUseCase
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def createUser(user: UserCreate, db: AsyncSession = Depends(get_db)):
    use_case = CreateUserUseCase()
    return await use_case.execute(db, user)


@router.get("/{user_id}")
async def getUserById(user_id: int, db: AsyncSession = Depends(get_db)):
    use_case = GetUseByIdUseCase()
    return await use_case.execute(db, user_id)
