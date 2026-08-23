![Python](https://www.python.org/static/img/python-logo.png)
# SkyLearn

SkyLearn — REST API для онлайн-платформы обучения.  
Проект разработан на Django и Django REST Framework.

Приложение работает в Docker Compose и включает:

- Django + Django REST Framework
- PostgreSQL
- Redis
- Celery Worker
- Celery Beat
- Poetry для управления зависимостями

---

## Технологии

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL 17
- Redis
- Celery
- Docker
- Docker Compose
- Poetry
- Stripe API

---

## Структура Docker Compose

Проект состоит из следующих сервисов:

| Сервис | Назначение | Порт |
|---|---|---|
| `web` | Django-приложение | `8000` |
| `db` | PostgreSQL | внутренний |
| `redis` | Redis | внутренний |
| `celery_worker` | Выполнение фоновых задач | внутренний |
| `celery_beat` | Запуск периодических задач | внутренний |

Внешний доступ требуется только к Django-приложению.

PostgreSQL и Redis доступны только внутри Docker-сети.

Данные PostgreSQL и Redis сохраняются в Docker volumes.

---

## Установка и запуск

### 1. Клонирование проекта

```bash
git clone <https://github.com/vadimsemenov53-crypto/SkyLearn>
cd SkyLearn
```

---

### 2. Создание файла .env

В проекте должен находиться файл .env.

Для создания собственного файла можно использовать .env.sample:

```bash
cp .env.sample .env
```

После этого необходимо указать необходимые значения переменных окружения.

---

### 3. Запуск через Docker Compose

```bash
docker-compose up -d --build
```

#### Проверить состояние контейнеров:

```bash
docker-compose ps
```
Ожидаемый результат:
- celery_beat      Up
- celery_worker    Up
- database         Up (healthy)
- redis            Up (healthy)
- skylearn         Up

### Остановка приложения:

```bash
docker compose down
```
##### Остановка с удалением volumes:

```bash
docker compose down -v
```

### Доступ к приложению:

```
http://localhost:8000/
```

----

### 4. Миграции.
Миграции Django выполняются автоматически при запуске контейнера web.

При необходимости миграции можно выполнить вручную:
```bash
docker compose exec web python manage.py migrate
```

Создание новых миграций:
```bash
docker compose exec web python manage.py makemigrations
```

----

### 5. Создание суперпользователя:
Создать администратора Django:

```bash
docker compose exec web python manage.py csu
```

---

### 6. Документация API:
#### Документация API доступна через Swagger.

- Адрес документации: http://localhost:8000/swagger/

- Также может быть доступна ReDoc: http://localhost:8000/redoc/

---
---

### Разработчик:
Vadim Semenov

GitHub: https://github.com/vadimsemenov53-crypto




