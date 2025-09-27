from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model.user import User
from app.users.use_cases.get_user_by_email_use_case import GetUserByEmailUseCase
from app.utils.security import verify_password


class VerifyUserCredentialsUseCase:

    @staticmethod
    async def execute(email: str, password: str, db: AsyncSession) -> Optional[User]:
        try:
            use_case = GetUserByEmailUseCase(db)
            user = await use_case.execute(email, db)

            is_valid = await verify_password(password, user.password)

            if not is_valid:
                return None
            return user
        except Exception:
            return None
