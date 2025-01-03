from re import fullmatch

from bs4 import BeautifulSoup


def get_forums(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    forums_div = soup.find("div", {"class": ["catalog-section-items", "intec-grid", "intec-grid-wrap", "intec-grid-a-v-stretch", "intec-grid-a-h-start"], "data-role": "items", "data-entity": "i-10-bitrix-catalog-section-catalog-tile-3rm-OQ3k9PHlVICg-1"})
    forums = forums_div.find_all("div", {"class": "catalog-section-item-wrapper"})
    forums = [forum.find("a", {"class": "btn-link"})["href"] for forum in forums]
    return forums


def get_participants(soup: BeautifulSoup) -> str:
    try:
        titles = list(map(lambda x: x.text.strip(), soup.find_all("div", {"class": "properties-preview-item-name"})))
        index = titles.index("Категории участников:")
        results = soup.find_all("div", {"class": "properties-preview-item-value"})[index].text.strip().replace("\xa0", "")
    except ValueError:
        results = "-"
    return results


def handle_forum(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    result = []
    # Title
    result.append(soup.find("h1", {"class": "forum-name"}).text.replace("\n", " ").strip())
    # Place
    result.append(soup.find("div", {"class": "forum-region"}).text.replace("\n", " ").strip())
    # Date
    result.append(soup.find("div", {"class": "period-event"}).text.replace("\n", " ").strip())
    # Application before
    result.append("-")
    # Category of participants
    result.append(get_participants(soup).replace("\n", " ").replace("\r", " "))
    # Project link
    result.append(soup.find("meta", {"name": "og:url"}).attrs["content"])
    # Month of project
    result.append(create_month(result[2]))
    # Platform(Росмолодёжь)
    result.append("Росмолодёжь")
    # End of application
    result.append(result[3])

    result = list(map(lambda x: "-" if x == "" else x, result))
    return result


def create_month(my_date: str) -> str:
    correct_date_to_num = {
        "январь": 1,
        "февраль": 2,
        "март": 3,
        "апрель": 4,
        "май": 5,
        "июнь": 6,
        "июль": 7,
        "август": 8,
        "сентябрь": 9,
        "октябрь": 10,
        "ноябрь": 11,
        "декабрь": 12
    }

    months = [
        "январь", "февраль", "март", "апрель", "май", "июнь",
        "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
    ]

    my_date = my_date.replace("–", "-").lower()

    if my_date == "":
        return "-"

    re_1 = r"(январь|февраль|март|апрель|май|июнь|июль|август|сентябрь|октябрь|ноябрь|декабрь) \d{4}"
    format1 = fullmatch(re_1, my_date)  # Сентябрь 2025

    re_2 = r"(январь|февраль|март|апрель|май|июнь|июль|август|сентябрь|октябрь|ноябрь|декабрь)-(январь|февраль|март|апрель|май|июнь|июль|август|сентябрь|октябрь|ноябрь|декабрь) ?\d*"
    format2 = fullmatch(re_2, my_date)  # Июнь-сентябрь 2025, Июнь-Сентябрь 2025, июнь-сентябрь 2025, июнь-Сентябрь 2025

    re_3 = r"(январь|февраль|март|апрель|май|июнь|июль|август|сентябрь|октябрь|ноябрь|декабрь) - (январь|февраль|март|апрель|май|июнь|июль|август|сентябрь|октябрь|ноябрь|декабрь) ?\d*"
    format3 = fullmatch(re_3, my_date)  # Июнь - сентябрь 2025, Июнь - Сентябрь 2025, июнь - сентябрь 2025, июнь - Сентябрь 2025

    result = []

    formats = list(map(lambda x: bool(x), [format1, format2, format3]))
    if formats == [False, False, False]:
        return "-"

    if formats[0]:
        result.append(months[correct_date_to_num[my_date.split(" ")[0]] - 1])
    elif formats[1] or formats[2]:
        if formats[1]:
            dates = my_date.split(" ")[0].split("-")
        elif formats[2]:
            dates = my_date[:-5].split(" - ")
        dates = list(map(lambda x: correct_date_to_num[x], dates))
        if dates[0] <= dates[1]:
            result.extend(months[dates[0] - 1:dates[1]])
        else:
            result.extend(months[dates[0] - 1:] + months[:dates[1]])

    if len(result) == 1:
        return result[0].title()
    else:
        result[0] = result[0].title()
        return ", ".join(result)
