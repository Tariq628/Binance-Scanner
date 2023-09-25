from celery import Celery
import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BinanceScanner.settings')

app = Celery('BinanceScanner')
app.conf.broker_url = 'redis://127.0.0.1:6379'
app.conf.result_backend = 'redis://127.0.0.1:6379/0'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def debug_task():
    print(f'Request: ')
