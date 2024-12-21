import asyncio

import httpx
from httpx import AsyncClient

from config import ROSMOL_FORUMS_PATH, ROSMOL_FORUMS_URL, ROSMOL_FORUMS_PARAM, SPREADSHEET_ID, SHEET_NAME
from utils import get_forums, handle_forum, request_html, authorize_google_sheets, write_to_google_sheet


async def main():
    request = httpx.get(ROSMOL_FORUMS_URL + "/" + ROSMOL_FORUMS_PATH, params=ROSMOL_FORUMS_PARAM)
    if request.status_code != 200:
        request.raise_for_status()

    html = request.text

    forums = get_forums(html)

    async with AsyncClient() as client:
        tasks = [asyncio.create_task(request_html(client, ROSMOL_FORUMS_URL + forum)) for forum in forums]
        forums_html = await asyncio.gather(*tasks)

    results = [handle_forum(html) for html in forums_html]
    print(results)

    service = authorize_google_sheets()
    write_to_google_sheet(service, SPREADSHEET_ID, SHEET_NAME, results)


if __name__ == "__main__":
    asyncio.run(main())
