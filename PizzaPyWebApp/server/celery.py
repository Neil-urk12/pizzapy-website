# PizzaPyWebApp/server/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'update-cache-every-day': {
        'task': 'app.tasks.update_cache_task',
        'schedule': crontab(hour=0, minute=0),    # Midnight PHT due to declaration of CELERY_TIMEZONE = 'Asia/Manila in settings.py
                                                    # however, it can still be override by the machine/system's timezone. so please align this with it
                                                    # example, my local is running on 12:50 PM (instead of 8:00 pm, so i ran this on 12:50 pm)
    },
}
