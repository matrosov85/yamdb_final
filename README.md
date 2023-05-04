[![Workflow Status](https://github.com/matrosov85/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/matrosov85/yamdb_final/actions/workflows/yamdb_workflow.yml)

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)


# YaMDb
Проект YaMDb собирает отзывы и оценки пользователей о различных произведениях. Произведения делятся на категории и жанры, список которых может быть расширен администратором. Доступ реализован через API-интерфейс.

## Проект развернут по адресу:
* http://matrosov85.ddns.net/api/v1/
* http://matrosov85.ddns.net/admin/
* http://matrosov85.ddns.net/redoc/


## Установка и запуск проекта

* Клонировать репозиторий и перейти в корневую директорию проекта:
```bash
git clone https://github.com/matrosov85/yamdb_final.git && cd yamdb_final
```

* Создать и активировать виртуальное окружение:
```bash
python -m venv venv && . venv/scripts/activate
```

* Обновить менеджер пакетов и установить зависимости:
```bash
python -m pip install --upgrade pip && pip install -r api_yamdb/requirements.txt
```

* Cоздать файл `infra/.env` со следующим содержимым:
```bash
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=postgres 
POSTGRES_PASSWORD=postgres 
DB_HOST=db 
DB_PORT=5432 
```

* Выполнить команду запуска контейнеров из директории `infra`:
```bash
cd infra && docker-compose up -d --build
```

* Создать и выполнить миграции:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

* Создать суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

* Собрать статику:
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

* Создать дамп базы данных:
```bash
docker-compose exec web python manage.py dumpdata > fixtures.json
```

* Для остановки контейнеров выполнить команду:
```bash
docker-compose down
```


## Примеры запросов к API

### Получение списка всех произведений

[GET-запрос]:

```bash
.../api/v1/titles/
```

Доступно без токена.

Параметры запроса:
- **category** (string) фильтрует по полю slug категории
- **genre**	(string) фильтрует по полю slug жанра
- **name** (string) фильтрует по названию произведения
- **year** (integer) фильтрует по году

Ответ API - (**200**):

```bash
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "name": "string",
            "year": 0,
            "rating": 0,
            "description": "string",
            "genre": [
                {
                    "name": "string",
                    "slug": "string"
                }
            ],
            "category": {
                "name": "string",
                "slug": "string"
            }
        }
    ]
}
```

### Регистрация нового пользователя

[POST-запрос]:

```bash
.../api/v1/auth/signup/
```

Присылает код подтверждения на переданный email. Код необходим для получения токена.

Body:

```bash
{
    "email" : "string", # Здесь ваши данные. До 254 символов, string
    "username" : "string" # Здесь ваши данные. До 150 символов, string
}
```

Ответ API - (**200**):

```bash
{
    "email": "string",
    "username": "string"
}
```

Другие возможные ответы:

- **400** Отсутствует обязательное поле или оно некорректно


### Добавление нового отзыва

Пользователь может оставить только один отзыв на произведение. Для доступа необходим jwt-токен.

[POST-запрос]:

```bash
.../api/v1/titles/{title_id}/reviews/
```

Параметры запроса:
- **title_id** (integer) ID произведения

Body:

```bash
{
    "text" : "example-text", # Текст отзыва, string
    "score" : [1...10] # Оценка в диапазоне от 1 до 10, integer
}
```

Ответ API - (**201**):

```bash
{
    "id": 0,
    "text": "example-text",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
```

Другие возможные ответы:

- **400** Отсутствует обязательное поле или оно некорректно
- **401** Необходим JWT-токен
- **404** Произведение не найдено