from httpx import AsyncClient


async def request_html(client: AsyncClient, url: str, params: dict = None) -> str:
    request = await client.get(url, params=params)
    if request.status_code != 200:
        request.raise_for_status()

    return request.text
