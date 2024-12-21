from bs4 import BeautifulSoup


def get_forums(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    forums_div = soup.find("div", {"class": ["catalog-section-items", "intec-grid", "intec-grid-wrap", "intec-grid-a-v-stretch", "intec-grid-a-h-start"], "data-role": "items", "data-entity": "i-10-bitrix-catalog-section-catalog-tile-3rm-OQ3k9PHlVICg-1"})
    forums = forums_div.find_all("div", {"class": "catalog-section-item-wrapper"})
    forums = [forum.find("a", {"class": "btn-link"})["href"] for forum in forums]
    return forums


def handle_forum(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    result = []
    title = soup.find("h1", {"class": "forum-name"}).text.replace("\n", "").strip()
    result.append(title)
    return result
