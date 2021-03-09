from celery import Celery

from app.core.config import celery_settings

CURRENT_MODULE_NAME = 'worker'

celery = Celery(main=CURRENT_MODULE_NAME)
celery.config_from_object(celery_settings)
