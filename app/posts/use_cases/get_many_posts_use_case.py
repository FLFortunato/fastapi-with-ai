import asyncio
from typing import List

from app.http_request.http_request import http_request


async def handle_fetch(url: str):

    allResults = []

    try:
        response = await http_request(
            url=url,
            method="get",
        )
        results = response.json()
        if len(results) > 0:
            allResults.append(results)
    except Exception as e:
        print(f"Failed to get url: {url}", e)
        return None
    return allResults


async def get_many_posts_use_case():

    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
    ]

    allRequests = [handle_fetch(url) for url in urls]

    results = await asyncio.gather(*allRequests)

    return results
