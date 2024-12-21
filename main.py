import asyncio

from httpx import AsyncClient

from config import ROSMOL_FORUMS_PATH, ROSMOL_FORUMS_URL
from utils import get_forums, handle_forum, request_html


async def main():
    async with AsyncClient() as client:
        html = await request_html(client, ROSMOL_FORUMS_URL + "/" + ROSMOL_FORUMS_PATH)

    forums = await asyncio.to_thread(get_forums, html)

    async with AsyncClient() as client:
        tasks = [asyncio.create_task(request_html(client, ROSMOL_FORUMS_URL + forum)) for forum in forums]
        forums_html = await asyncio.gather(*tasks)

    tasks = [asyncio.create_task(asyncio.to_thread(handle_forum, html)) for html in forums_html]
    result = await asyncio.gather(*tasks)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
