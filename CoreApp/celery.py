import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','CoreApp.settings')
app = Celery('CoreApp', broker='redis://localhost:6379/0', broker_connection_retry_on_startup=True)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

app.autodiscover_tasks()