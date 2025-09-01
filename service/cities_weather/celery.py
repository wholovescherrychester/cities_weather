import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cities_weather.settings')

app = Celery('cities_weather')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()