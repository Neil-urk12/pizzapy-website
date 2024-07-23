from django.apps import AppConfig
from django.core.cache import cache
from .utils import get_valid_access_token, fetch_events, extract_events
from .cache_utils import update_cache_for_groups


class AppServerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        # Populate cache for all three groups when the server starts
        print("AppConfig ready method called.")
        update_cache_for_groups()