from celery import shared_task
from django.core.cache import cache
from .cache_utils import update_cache_for_groups

@shared_task
def update_cache_task():
    print('checking update_cache_task---')
    cache.clear()
    print('cache clear')
    update_cache_for_groups()
    print('Cache updated!')