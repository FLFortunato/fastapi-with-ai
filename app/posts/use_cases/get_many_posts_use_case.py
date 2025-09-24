from app.http_request.http_request import http_request


async def get_many_posts_use_case():

    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "http://jsonplaceholder.typiode.com/2",
        "https://jsonplaceholder.typicode.com/posts/3",
    ]

    allResults = []

    for url in urls:
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

    return allResults
