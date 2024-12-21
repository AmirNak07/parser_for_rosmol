import asyncio

import httpx
from httpx import AsyncClient
from loguru import logger

from config import ROSMOL_FORUMS_PATH, ROSMOL_FORUMS_URL, ROSMOL_FORUMS_PARAM, SPREADSHEET_ID, SHEET_NAME, LOGS_CONFIG
from utils import get_forums, handle_forum, request_html, authorize_google_sheets, write_to_google_sheet


logger.remove()
logger.configure(**LOGS_CONFIG)


@logger.catch
async def main():
    logger.info("Start parsing")
    request = httpx.get(ROSMOL_FORUMS_URL + "/" + ROSMOL_FORUMS_PATH, params=ROSMOL_FORUMS_PARAM)
    if request.status_code != 200:
        request.raise_for_status()
    html = request.text
    logger.debug("Get forums list html")

    forums = get_forums(html)
    logger.debug(f"Found {len(forums)} forums")

    async with AsyncClient() as client:
        tasks = [asyncio.create_task(request_html(client, ROSMOL_FORUMS_URL + forum)) for forum in forums]
        forums_html = await asyncio.gather(*tasks)
    logger.debug("Get forums html")

    results = [handle_forum(html) for html in forums_html]
    logger.debug("Handle forums html")

    service = authorize_google_sheets()
    write_to_google_sheet(service, SPREADSHEET_ID, SHEET_NAME, results)
    logger.debug("Write to google sheet")
    logger.info("End parsing")


if __name__ == "__main__":
    asyncio.run(main())
