# tests/units/utils/test_security.py
import pytest

from app.utils.security import hash_password, verify_password


@pytest.mark.asyncio
async def test_hash_password_generates_different_value():
    password = "minha_senha123"

    hashed = await hash_password(password)
    assert hashed != password  # hash nunca deve ser igual ao original
    assert isinstance(hashed, str)


@pytest.mark.asyncio
async def test_verify_password_success():
    password = "senha_forte"
    hashed = await hash_password(password)

    is_valid = await verify_password(password, hashed)
    assert is_valid is True


@pytest.mark.asyncio
async def test_verify_password_failure():
    password = "senha_forte"
    hashed = await hash_password(password)

    is_valid = await verify_password("senha_errada", hashed)
    assert is_valid is False
