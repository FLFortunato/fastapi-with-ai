from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema.token import Token
from app.auth.use_cases.create_access_token_use_case import CreateAccessTokenUseCase
from app.auth.use_cases.verify_user_credentials_use_case import (
    VerifyUserCredentialsUseCase,
)


class LoginUseCase:

    @staticmethod
    async def execute(data: OAuth2PasswordRequestForm, db: AsyncSession) -> Token:

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user = await VerifyUserCredentialsUseCase.execute(
            data.username, data.password, db
        )

        if not user or not user.is_active:
            raise credentials_exception
        create_tokens = CreateAccessTokenUseCase()
        token = create_tokens.execute({"sub": user.email})
        return token
