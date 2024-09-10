# API благотворительных проектов для котиков

Этот проект предоставляет API для управления благотворительными проектами и пожертвованиями. Он создан с использованием FastAPI и SQLAlchemy с поддержкой асинхронности.

## Возможности

- Создание, обновление и удаление благотворительных проектов.
- Пожертвования на благотворительные проекты.
- Обеспечение уникальности названий проектов и выполнение различных бизнес-правил.
- Обработка аутентификации и авторизации пользователей.

## Требования

- Python 3.8+
- SQLite

## Установка

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/charity-project-api.git
    cd charity-project-api
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Настройте переменные окружения:

    Создайте файл `.env` в корневой директории проекта и добавьте ваши настройки:

    ```env
    DATABASE_URL=sqlite:///./test.db
    SECRET_KEY=your_secret_key
    ```

5. Выполните миграции базы данных:

    ```bash
    alembic upgrade head
    ```

## Использование

1. Запустите сервер FastAPI:

    ```bash
    uvicorn app.main:app --reload
    ```

2. Откройте браузер и перейдите по адресу `http://localhost:8000/docs`, чтобы получить доступ к интерактивной документации API.

## Структура проекта

```plaintext
.
├── app
│   ├── api
│   │   ├── endpoints
│   │   │   ├── charity_project.py
│   │   │   └── donation.py
│   │   └── validators.py
│   ├── core
│   │   ├── config.py
│   │   ├── db.py
│   │   └── user.py
│   ├── crud
│   │   ├── base.py
│   │   ├── charity_project.py
│   │   └── donation.py
│   ├── models
│   │   ├── base.py
│   │   ├── charity_project.py
│   │   └── donation.py
│   ├── schemas
│   │   ├── charity_project.py
│   │   └── donation.py
│   └── services
│       └── investment.py
├── alembic
│   ├── versions
│   └── env.py
├── tests
│   ├── test_charity_project.py
│   └── test_donation.py
├── .env.example
├── alembic.ini
├── README.md
└── requirements.txt
```

# API Endpoints

## Благотворительные проекты

- `POST /charity_projects/`: Создание нового благотворительного проекта.
- `PATCH /charity_projects/{project_id}`: Частичное обновление благотворительного проекта.
- `GET /charity_projects/`: Получение списка всех благотворительных проектов.
- `DELETE /charity_projects/{project_id}`: Удаление благотворительного проекта.

## Пожертвования

- `POST /donations/`: Создание нового пожертвования.
- `GET /donations/my`: Получение всех пожертвований, сделанных текущим пользователем.

## Валидация и бизнес-логика

Проверка и валидация данных реализованы в `app/services/investment.py`. Основные функции включают:

- `check_project_name`: Убедиться, что название проекта уникально.
- `check_project_exists`: Проверить существование проекта.
- `check_project_activeness`: Проверить активность проекта.
- `check_project_investment`: Убедиться, что проект не имеет инвестиций перед удалением.
- `check_amount_update`: Проверить обновление суммы для проекта.

## Лицензия

Этот проект лицензирован по лицензии MIT. См. файл `LICENSE` для получения дополнительной информации.# API благотворительных проектов для котиков
