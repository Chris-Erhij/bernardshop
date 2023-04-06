import os
from celery import Celery
from typing import Type

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'bernardshop.settings')
app: Type = Celery('bernardshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
