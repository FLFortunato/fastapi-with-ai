from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth.use_cases.validate_credentials_use_case import (
    ValidateCredentialsUseCase,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class ValidateAuthentication:

    @staticmethod
    async def execute(token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        validate_token = ValidateCredentialsUseCase()
        try:
            email = validate_token.execute(token)
            return email
        except Exception:
            raise credentials_exception
