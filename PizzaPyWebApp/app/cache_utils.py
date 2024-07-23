from django.core.cache import cache
from .utils import get_valid_access_token, fetch_events, extract_events

def update_cache_for_groups():
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
        return print('no token')

    for group_name in group_names:
        variables = {"urlname": group_name}
        data = fetch_events(query, token, variables)
        if data:
            events = extract_events(data, "upcomingEvents")
            cache.set(f'events_{group_name}', events, timeout=86400)
