# MISE Restaurant Booking API

REST API для онлайн-бронирования столика в ресторане.

## Запуск через Docker Compose

```bash
docker compose up --build
```

API будет доступно по адресу `http://127.0.0.1:8000`, Swagger UI — на `http://127.0.0.1:8000/docs`, ReDoc — на `http://127.0.0.1:8000/redoc`. SQLite хранится в именованном volume `booking_data` и сохраняется между перезапусками контейнера. При старте entrypoint сначала применяет Alembic-миграции, затем выполняет seed и только после этого запускает Uvicorn.

Seed включён по умолчанию и идемпотентно добавляет три демонстрационные брони на даты относительно текущего дня. Чтобы отключить его, измените `seed_demo_data: bool = True` на `seed_demo_data: bool = False` в `app/core/config.py` перед сборкой образа.

## Локальный запуск тестов

Для запуска через `uv` требуются Python 3.11 или новее и [uv](https://docs.astral.sh/uv/):

```bash
uv sync --dev
uv run pytest -q
```

Для запуска через `pip` требуются Python 3.11 или новее и стандартный модуль `venv`:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install \
  aiosqlite alembic fastapi pydantic pydantic-settings \
  'sqlalchemy[asyncio]' uvicorn httpx pytest pytest-asyncio
python -m pytest -q
```

## API

| Метод | Путь | Описание |
|---|---|---|
| `POST` | `/bookings` | Создать бронь, успешный ответ `201 Created` |
| `GET` | `/bookings` | Получить список броней |
| `GET` | `/bookings/{booking_id}` | Получить бронь или ответ `404` |
| `DELETE` | `/bookings/{booking_id}` | Мягко отменить бронь |

`GET /bookings` принимает необязательный фильтр `date=YYYY-MM-DD`, а также параметры `offset` и `limit`


## Ключевые решения

Отмена изменяет статус записи вместо удаления и освобождает слот для новой брони. Рабочие значения конфигурации по умолчанию позволяют запустить проект без `.env`, что упрощает проверку тестового задания.

## Что бы еще доделал

- Добавил модель ресторанных столов с вместимостью и автоматическим подбором подходящего стола
- Реализовал авторизацию и роли
- Заменил SQLite на PostgreSQL
- Добавил логирование
