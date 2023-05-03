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


## Установка

* Клонировать репозиторий:
```bash
git clone <url>
```

* Перейти в корневую директорию проекта:
```bash
cd yamdb_final
```

* Создать и активировать виртуальное окружение:
```bash
python -m venv venv && . venv/scripts/activate
```

* Обновить менеджер пакетов и установить зависимости:
```bash
python -m pip install --upgrade pip && pip install -r api_yamdb/requirements.txt
```

* Cоздать файл `infra/.env`:
```bash
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=postgres 
POSTGRES_PASSWORD=postgres 
DB_HOST=db 
DB_PORT=5432 
```

## Настройка удаленного сервера

* Подключиться к удаленному серверу:
```bash
ssh <username>@<host>
```

* Обновить менеджер пакетов и системные пакеты:
```bash
sudo apt update && sudo apt upgrade -y
```

* Установить `docker`:
```bash
sudo apt install docker.io
```

* Установить `docker-compose`:
```bash
sudo curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

* Создать директорию `nginx`:
```bash
mkdir nginx/
```

* Скопировать файлы `docker-compose.yaml` и `nginx/defult.conf` из локальной директории `infra` проекта на сервер:
```bash
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yaml
scp default.conf <username>@<host>:/home/<username>/nginx/default.conf
```

* Добавить переменные в `Github/Settings/Secrets and variables/Actions/Secrets`:
```bash
DOCKER_USERNAME       # логин DockerHub
DOCKER_PASSWORD       # пароль DockerHub

USER                  # логин для подключения к серверу
HOST                  # IP-адрес сервера
SSH_KEY               # приватный SSH-ключ компьютера, имеющего доступ к серверу (cat ~/.ssh/id_rsa)
PASSPHRASE            # пароль от SSH-ключа

TELEGRAM_TO           # ID телеграм-аккаунта (@userinfobot)
TELEGRAM_TOKEN        # токен телеграм бота (@botfather)

DB_ENGINE             # django.db.backends.postgresql
DB_NAME               # название БД (postgres)
DB_HOST               # название контейнера (db)
DB_PORT               # порт для подключения к БД (5432)
POSTGRES_USER         # логин для подключения к БД (postgres)
POSTGRES_PASSWORD     # пароль для подключения к БД (postgres)
```

## Запуск

* Выполнить push в ветку `main`:
```bash
git add .
git commit -m 'комментарий'
git push
```

* После выполнения команды `git push` будет выполнен `workflow`, состоящий из следующих задач:
  * проверка кода на соответствие стандарту `PEP8` (с помощью пакета `flake8`) и запуск `pytest` из репозитория `yamdb_final`
  * сборка и доставка докер-образа для контейнера `web` на `Docker Hub`
  * автоматический деплой проекта на сервер
  * отправка уведомления в `Telegram` о том, что процесс деплоя успешно завершился

* После деплоя зайти на сервер и выполнить окончательные настройки:
  * создать миграции:
  ```bash
  sudo docker-compose exec web python manage.py makemigrations
  ```
  * выполнить миграции:
  ```bash
  sudo docker-compose exec web python manage.py migrate
  ```
  * создать суперпользователя:
  ```bash
  sudo docker-compose exec web python manage.py createsuperuser
  ```
  * собрать статику:
  ```bash
  sudo docker-compose exec web python manage.py collecstatic --no-input
  ```
  * наполнить базу данных:
  ```bash
  sudo docker-compose exec web python manage.py loaddata fixtures.json
  ```
  * остановить контейнеры:
  ```bash
  sudo docker-compose down
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
  "results": [...]
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

Подробная документация описана в ReDoc