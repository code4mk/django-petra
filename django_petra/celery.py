# celery_config.py

from __future__ import absolute_import, unicode_literals
from drf_friend.scheduler.schedule import bind_beat_schedule
import os
from celery import Celery
from django.apps import apps
import importlib

def configure_celery(project_name, type = 'redis'):

    # Set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')

    # Create a Celery instance.
    app = Celery(project_name)

    # Load task modules from all registered Django app configs.
    app.config_from_object('django.conf:settings', namespace='CELERY')

    app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

    app.conf.broker_url = os.environ.get('CELERY_BROKER')

    # Dynamically import schedules from {project_name}.friend_scheduler
    schedules_module = importlib.import_module(f'{project_name}.friend_config.scheduler')
    app.conf.beat_schedule = bind_beat_schedule(schedules=schedules_module.schedules)

    # RedBeat Configuration
    if type == 'redis':
        app.conf.redbeat_redis_url = os.environ.get('CELERY_BROKER')
        # Use RedBeatScheduler
        app.conf.beat_scheduler = 'redbeat.RedBeatScheduler'
    
    return app
