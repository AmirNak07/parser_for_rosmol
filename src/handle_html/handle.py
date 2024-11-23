from bs4 import BeautifulSoup
from loguru import logger

from utils import (
    create_month,
    create_project_link,
    create_request,
    delete_old_projects,
    put_application,
    put_categories,
)


@logger.catch
def create_projects(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    logger.debug("Процесс парсинга...")
    cards = []
    card = []

    if soup.find_all("div", class_="catalog-section-item-base") == []:
        logger.warning("Не было найдено ни одно мероприятие")
        return [["title", "place", "date", "application_before", "category_of_participants",
                 "project_link", "month_of_project", "platform", "end_of_application"]]

    for i in range(len(soup.find_all("div", class_="catalog-section-item-base"))):
        logger.debug(f"Поиск информации в сайте: {create_project_link(soup.find_all(
            "div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True))}")

        # Название
        card.append(" ".join(soup.find_all(
            "div", class_="catalog-section-item-name")[i].text.split()))

        # Место
        card.append(" ".join(soup.find_all(
            "div", class_="catalog-section-forum-region")[i].text.split()))

        # Даты
        card.append(soup.find_all(
            "div", class_="period-event-tile-date")[i].text)

        # Заявка до
        card.append(put_application(create_request(create_project_link(soup.find_all(
            "div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True)))))

        # Категория участников
        card.append(put_categories(create_request(create_project_link(soup.find_all("div", class_="catalog-section-item-name")
                    [i].findChildren("a", recursive=False, href=True)))).replace("\r", "").replace("\n", ""))

        # Ссылка не проект
        card.append(create_project_link(soup.find_all(
            "div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True)))

        # Проекты по месяцам
        card.append(create_month(
            str(soup.find_all("div", class_="period-event-tile-date")[i].text)))

        # Платформа
        card.append("Росмолодежь")

        # Конец заявки для календаря = заявка до
        card.append(put_application(create_request(create_project_link(soup.find_all(
            "div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True)))))

        cards.append(card.copy())
        card.clear()

    result = delete_old_projects(cards)

    logger.debug(f"Мероприятия готовы: {result}")
    return result
