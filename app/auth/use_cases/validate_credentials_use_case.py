from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import ALGORITHM, JWT_SECRET_KEY


class ValidateCredentialsUseCase:

    def execute(self, token: str):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM or ""])

            email: str = payload.get("sub")
            if email is None:
                raise ValueError("No subject in token")
            return email
        except jwt.DecodeError as e:
            raise ValueError("Invalid or expired token")
