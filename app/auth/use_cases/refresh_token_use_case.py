import logging

import jwt
from fastapi import HTTPException, status

from app.auth.use_cases.create_access_token_use_case import CreateAccessTokenUseCase
from app.core.config import (
    ALGORITHM,
    REFRESH_JWT_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_DAYS,
)

logger = logging.getLogger(__name__)


class RefreshTokenUseCase:

    @staticmethod
    def execute(refresh_token: str):
        try:
            if not REFRESH_TOKEN_EXPIRE_DAYS:
                raise ValueError("REFRESH_TOKEN_EXPIRE_DAYS is not set")
            if not ALGORITHM:
                raise ValueError("ALGORITHM is not set")

            payload = jwt.decode(
                refresh_token,
                REFRESH_JWT_SECRET_KEY,
                algorithms=[ALGORITHM or ""],
            )

            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired refresh token"
            )
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid refresh token error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )
        create_access_token = CreateAccessTokenUseCase()
        new_access_token = create_access_token.execute({"sub": email})
        return new_access_token
