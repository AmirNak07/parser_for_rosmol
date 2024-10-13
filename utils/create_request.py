import httpx
from bs4 import BeautifulSoup

def create_request(link: str) -> str:
    response = httpx.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        all_info_title = [i.text.strip().replace(u'\xa0', u' ') for i in soup.find_all(
            "div", class_="properties-preview-item-name")]
        all_info_value = [i.text.strip().replace(u'\xa0', u' ') for i in soup.find_all(
            "div", class_="properties-preview-item-value")]
        all_info = list(zip(all_info_title, all_info_value))
        return all_info