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

## Первоначальная настройка сервера

Перед первым запуском проекта на сервере необходимо один раз создать файл .env в корневой директории проекта:

- cd ~/SkyLearn
- nano .env

Заполнить его переменными, указанными в .env.template.

После создания .env проект можно запустить:

docker compose up -d

---

### Автоматический деплой

После первоначальной настройки .env дальнейший деплой 
выполняется автоматически через GitHub Actions.

При "push" в ветку -main- workflow:

- Запускает тесты.
- Запускает Flake8.
- Собирает Docker-образ.
- Загружает образ в Docker Hub.
- Подключается к серверу по SSH.
- Обновляет код проекта.
- Загружает новую версию Docker-образа.
- Перезапускает контейнеры.

-- Файл .env при этом не удаляется и не перезаписывается, поэтому создавать его повторно после каждого деплоя не требуется.

---

### Переменные GitHub Secrets

Для работы CI/CD в настройках репозитория GitHub необходимо добавить:

- DOCKER_HUB_USERNAME — имя пользователя Docker Hub.
- DOCKER_HUB_ACCESS_TOKEN — Access Token Docker Hub.
- SSH_USER — пользователь для подключения к серверу.
- SERVER_IP — публичный IP-адрес сервера.
- SSH_KEY — приватный SSH-ключ для подключения к серверу.

---

#### Безопасность

В репозитории запрещено хранить:

```
.env
приватные SSH-ключи
пароли
токены
API-ключи
другие чувствительные данные
```

Для проверки:

```
git check-ignore .env
```

- Команда должна показать --> .env

### Разработчик:
Vadim Semenov

GitHub: https://github.com/vadimsemenov53-crypto




