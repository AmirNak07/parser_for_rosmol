# Парсер Росмолодёжи

## Описание

Данный код парсит форумы с открытой регистрацией из сайта [Росмолодёжи](https://events.myrosmol.ru) и возвращает в виде JSON файла.

## Элементы JSON

Описание всех элементов, входящие в JSON файл:

| Название | Описание |
| ------ | ------ |
| title | Название форума |
| place | Место проведения форума |
| date | Даты проведения |
| application_before | Регистрация до(дата) |
| category_of_participants | Категория участников |
| project_link | Ссылка на форум |
| end_of_application | = application_before(необязательное поле) |

## Установка

1. Склонировать репозиторий

    ```bash
    git clone link_to_repository
    ```

2. Настроить перменные среды

    Создать файл ".env" в папке config и заполнить его по примеру из файла ".env.example". Пример файла ".env":

    ```env
    ID_TABLE=2434242_fasdkljklfsa_kljfdkj;-41dsggas
    SPREADSHEET=Лист1
    ```

3. Создать файл аутенфикации OAuth

    В директорию "config" переместите(скопируете) файл с вашими данными из Google Workplace с вашим проектом и назовите "credentials.json"

## Запуск

Создание образа:

```bash
docker build -t rosmol_parser_image . 
```

Запуск образа:

```bash
docker run -d --name rosmol_parser rosmol_parser_image:latest 
```

Примечание: Данная версия работает с браузером Firefox
