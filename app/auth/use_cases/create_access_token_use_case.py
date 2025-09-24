from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from app.auth.schema.token import Token, TokenData
from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    JWT_SECRET_KEY,
    REFRESH_JWT_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


class CreateAccessTokenUseCase:

    def execute(
        self,
        data: dict,
    ) -> Token:

        access_token = self.create_access_token(data)
        refresh_token = self.create_refresh_token(data)

        return Token(
            access_token=access_token, token_type="bearer", refresh_token=refresh_token
        )

    def create_access_token(self, data: dict) -> str:
        if not JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY is not set")
        if not ALGORITHM:
            raise ValueError("ALGORITHM is not set")

        if not ACCESS_TOKEN_EXPIRE_MINUTES:
            raise ValueError("ALGORITHM is not set")

        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        if not REFRESH_TOKEN_EXPIRE_DAYS:
            raise ValueError("REFRESH_TOKEN_EXPIRE_DAYS is not set")
        if not ALGORITHM:
            raise ValueError("ALGORITHM is not set")

        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            days=int(REFRESH_TOKEN_EXPIRE_DAYS)
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, REFRESH_JWT_SECRET_KEY, algorithm=ALGORITHM)
        print(f"{encoded_jwt}, {REFRESH_TOKEN_EXPIRE_DAYS},{ALGORITHM}")
        return encoded_jwt
