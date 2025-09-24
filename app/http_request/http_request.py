from typing import Any, Literal, Optional

from httpx import AsyncClient, Headers


async def http_request(
    url: str,
    method: Literal["get", "put", "post", "delete"],
    data: Optional[Any] = None,
    headers: Optional[Headers] = None,
):
    async with AsyncClient() as client:
        response = await client.request(
            method=method, url=url, data=data, headers=headers
        )
        return response
