from celery import Celery
from celery.schedules import crontab

from configs.config import redis_settings

redis_url = (
    f"redis://{redis_settings.REDIS_HOST}:{redis_settings.REDIS_PORT}/0"
)
celery_app = Celery(
    "tasks", broker=redis_url, backend=redis_url, include=["tasks.tasks"]
)
celery_app.conf.update(task_track_started=True)
celery_app.conf.beat_schedule = {
    "update_subscribed_products": {
        "task": "tasks.tasks.update_subcribed_products_task",
        "schedule": crontab(minute="*/30"),
    },
}
