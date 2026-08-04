import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "innotter.settings")

app = Celery("innotter")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "unblock-pages-daily": {
        "task": "pages.tasks.unblock_expired_pages",
        "schedule": crontab(hour=0, minute=0),
    },
}
