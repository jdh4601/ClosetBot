"""Celery configuration"""

from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "fasion",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.services.analysis.worker",
    ],
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,  # 10 minutes max per task
    worker_prefetch_multiplier=1,  # Process one task at a time per worker
    broker_connection_retry_on_startup=True,
)

# Task routing
celery_app.conf.task_routes = {
    "app.services.analysis.worker.*": {"queue": "analysis"},
}

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "cleanup-expired-data": {
        "task": "app.services.analysis.worker.cleanup_expired_data",
        "schedule": 86400.0,  # Run once per day
    },
}
