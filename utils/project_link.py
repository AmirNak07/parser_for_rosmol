def create_project_link(link: str) -> str:
    link = str(link).split()[1].replace('href="', "").replace('">', "")
    return "https://events.myrosmol.ru" + link
