
---

## bot_service/README.md

```md
# Bot Service

Telegram bot service с Celery, Redis и RabbitMQ.

## Запуск бота

```bash
python -m app.main

## Запуск worker

```bash
celery -A app.infra.celery_app.celery_app worker --loglevel=info
