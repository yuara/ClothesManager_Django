from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery(
    "config",
    broker=os.environ.get("REDIS_URL", "redis://localhost:6379"),
    # backend=os.environ.get("REDIS_URL", "redis://localhost:6379"),
)

app.conf.result_backend = os.environ.get("REDIS_URL", "redis://localhost:6379")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Executes tasks with crontab periodically.
app.conf.beat_schedule = {
    "scrape-forecast-every-hour": {
        "task": "config.celery.scrape_forecast",
        "schedule": crontab(hour="*", minute=55),  # Executes every hour
    },
    "test-periodical-task": {"task": "add", "schedule": crontab(minute="*")},
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@app.task(name="add")
def add():
    print("Start Add Method")
    return 3


@app.task()
def scrape_forecast():
    from scraping.crawl import run_spider

    return run_spider()


@app.task()
def sc():
    from scraping.crawl import runs

    return runs()
