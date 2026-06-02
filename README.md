# Двухсервисная система LLM-консультаций

Микросервисная система для взаимодействия с большой языковой моделью через Telegram-бота.

## Возможности

* JWT-аутентификация пользователей
* Telegram-бот на aiogram
* Интеграция с OpenRouter API
* Асинхронная обработка LLM-запросов через Celery
* Очереди RabbitMQ
* Хранение токенов в Redis
* FastAPI backend
* Docker для Redis и RabbitMQ

---

# Архитектура

```text
Telegram User
     ↓
Bot Service (aiogram)
     ↓
RabbitMQ
     ↓
Celery Worker
     ↓
OpenRouter API
     ↓
Telegram User

Auth Service → JWT → Bot Service
Redis → хранение JWT токенов
```

---

# Стек технологий

* Python 3.12
* FastAPI
* aiogram
* Redis
* RabbitMQ
* Celery
* OpenRouter API
* SQLite
* Docker
* JWT
* uv

---

# Структура проекта (верхний уровень)

```text
llm-consulting-system/
│
├── auth_service/
├── bot_service/
├── screenshots/
├── .gitignore
└── README.md

```

---

# Auth Service

Auth Service отвечает за:

* регистрацию пользователей
* логин
* генерацию JWT
* проверку текущего пользователя

## Основные endpoints

### Регистрация

```http
POST /auth/register
```

### Логин

```http
POST /auth/login
```

### Текущий пользователь

```http
GET /auth/me
```

Swagger:

```text
http://localhost:8000/docs
```

---

# Bot Service

Bot Service отвечает за:

* Telegram-бота
* JWT-авторизацию
* отправку задач в RabbitMQ
* взаимодействие с Celery worker
* получение ответов от OpenRouter

---

# Запуск проекта

## Клонирование репозитория

```bash
git clone https://github.com/KiraraGho/llm-consulting-system.git
cd llm-consulting-system
```

---

# Redis

```bash
docker run -d --name redis -p 6379:6379 redis
```

---

# RabbitMQ

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

RabbitMQ UI:

```text
http://localhost:15672
```

Логин/пароль:

```text
guest
guest
```

---

# Запуск Auth Service

```bash
cd auth_service

uv venv
source .venv/bin/activate

uv pip compile pyproject.toml -o requirements.txt
uv pip install -r requirements.txt

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

# Запуск Bot Service

```bash
cd bot_service

uv venv
source .venv/bin/activate

uv pip compile pyproject.toml -o requirements.txt
uv pip install -r requirements.txt

python -m app.main
```

---

# Запуск Celery Worker

```bash
cd bot_service

source .venv/bin/activate

celery -A app.infra.celery_app.celery_app worker --loglevel=info
```

---

# Переменные окружения

## auth_service/.env

```env
JWT_SECRET=change_me_super_secret
JWT_ALG=HS256
```

## bot_service/.env

```env
TELEGRAM_BOT_TOKEN=
OPENROUTER_API_KEY=

JWT_SECRET=change_me_super_secret
JWT_ALG=HS256

REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://guest:guest@localhost:5672//
```

---

# Демонстрация работы

## Swagger Auth Service

![Swagger](screenshots/swagger.png)

## Telegram Bot

![Telegram Bot](screenshots/telegrambot.png)

## RabbitMQ UI

![RabbitMQ](screenshots/rabbitmq.png)

## Docker Containers

![Docker](screenshots/docker.png)

## Celery Worker

![Celery](screenshots/celery.png)

---

# JWT Flow

1. Пользователь логинится через Auth Service
2. Получает JWT
3. Отправляет JWT Telegram-боту
4. Bot Service проверяет JWT
5. JWT сохраняется в Redis

---

# LLM Request Flow

1. Пользователь отправляет сообщение боту
2. Bot Service отправляет задачу в RabbitMQ
3. Celery worker получает задачу
4. Worker обращается к OpenRouter API
5. Ответ возвращается пользователю в Telegram

---

# Автор

Виктория Шинкаренко, студент группы М25-555
