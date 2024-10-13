def put_categories(response: str) -> str:
    for i in response:
        if i[0] == "Категории участников:":
            return i[1]
    return "-"