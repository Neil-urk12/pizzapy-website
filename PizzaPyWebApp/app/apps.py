from django.apps import AppConfig
from django.core.cache import cache
from .utils import get_valid_access_token, fetch_events, extract_events


class AppServerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        # Populate cache for all three groups when the server starts
        print("AppConfig ready method called.")
        self.update_cache_for_groups()

    def update_cache_for_groups(self):
        print("Updating cache for groups...")
        group_names = [
            "pizzapy-ph",
            "cebu-city-cybersecurity-center-c4",
            "p5-management-hub",
        ]

        query = """
        query ($urlname: String!) {
            groupByUrlname(urlname: $urlname) {
                upcomingEvents(input: { first: 3 }, sortOrder: ASC) {
                    edges {
                        node {
                            id
                            title
                            description
                            eventType
                            images {
                                source
                            }
                            venue {
                                address
                                city
                                postalCode
                            }
                            createdAt
                            dateTime
                            endTime
                            timezone
                            going
                            shortUrl
                            host {
                                name
                                username
                                email
                                memberPhoto {
                                    id
                                    baseUrl
                                    preview
                                    source
                                }
                                memberUrl
                                organizedGroupCount
                            }
                        }
                    }
                }
            }
        }
        """
        token = get_valid_access_token()
        if not token:
            return

        for group_name in group_names:
            variables = {"urlname": group_name}
            data = fetch_events(query, token, variables)
            if data:
                events = extract_events(data, "upcomingEvents")
                cache.set(f'events_{group_name}', events, timeout=86400)  # Cache for 24 hours



