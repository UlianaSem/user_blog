# User blog

## Описание проекта

Проект, реализующий блог пользователей с возможностью создавать и удалять посты, отмечать посты прочитанными, а также подписываться на блоги других пользователей.

Осуществлена ежедневная email рассылка пяти последних записей в ленте.

## Технологии

- Linux
- Python
- Poetry
- Django
- DRF
- PostgreSQL
- Redis
- Celery
- Docker
- Docker Compose

## Зависимости

Зависимости, необходимые для работы проекта, указаны в файле pyproject.toml.

## Документация

Документация находится по ссылкам:
1. Для загрузки schema.yaml `api/schema/`
2. Swagger `api/schema/swagger-ui`
3. Redoc `api/schema/redoc/`

## Как запустить проект

Для запуска проекта необходимо выполнить следующие шаги:
1. При необходимости установите Docker и Docker Compose на компьютер с помощью инструкции https://docs.docker.com/engine/install/
2. Cклонируйте репозиторий себе на компьютер
3. Создайте файл .env и заполните его, используя образец из файла .env.example
4. Соберите образ с помощью команды `docker-compose build`
5. Запустите контейнеры с помощью команды `docker-compose up`

## Файл .env.example

1. `DATABASES_NAME, DATABASES_USER, DATABASES_PASSWORD, DATABASES_HOST` - данные для подключения к БД
2. `EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_SSL` - данные для осуществления Email рассылки
3. `REDIS_HOST` - хост Redis
4. `SECRET_KEY, DEBUG, ALLOWED_HOSTS`

## Авторы

UlianaSem

## Связь с авторами

https://github.com/UlianaSem/
