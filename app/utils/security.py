# app/utils/security.py
import asyncio
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash_password(password: str) -> str:
    """Gera hash de senha de forma assíncrona para não bloquear o event loop."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, pwd_context.hash, password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha bate com o hash de forma assíncrona."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, pwd_context.verify, plain_password, hashed_password
    )
