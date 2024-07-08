from celery import Celery
from api.config import config

celery = Celery('tasks', broker=config.celery_broker_url, backend=config.celery_result_backend)
