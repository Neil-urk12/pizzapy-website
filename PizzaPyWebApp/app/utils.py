import requests
from django.core.cache import cache
from django.conf import settings
import jwt
import datetime
import time

# Global variable to store the access token and its expiration time
TOKEN_INFO = {
    "access_token": None,
    "expires_at": 0
}

def create_signed_jwt():
    private_key = open(settings.MEETUP_PRIVATE_KEY_PATH, 'r').read()
    
    payload = {
            'sub': settings.MEMBER_ID,
            'iss': settings.OAUTH_KEY,
            'aud': 'api.meetup.com',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        }

    
    token = jwt.encode(payload, private_key, algorithm='RS256')
    # print(f"Created JWT: {token}")
    return token
    

def get_access_token(signed_jwt):
    token_url = "https://secure.meetup.com/oauth2/access"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": signed_jwt
    }
    
    response = requests.post(token_url, data=payload, headers=headers)
    
    # print(f"Request payload: {payload}")
    # print(f"Response status code: {response.status_code}")
    # print(f"Response content: {response.text}")

    if response.status_code == 200:
        print(response.json().get("access_token"))
        return response.json().get("access_token")
    if response.status_code == 400:
        print(f"wrong na")
    else:
        print(f"Failed to get access token: {response.text}")
        return None

def is_token_expired():
    """Check if the access token is expired."""
    return time.time() >= TOKEN_INFO['expires_at']

def refresh_access_token():
    """Refresh the access token and update the TOKEN_INFO."""
    signed_jwt = create_signed_jwt()
    new_token = get_access_token(signed_jwt)
    if new_token:
        TOKEN_INFO['access_token'] = new_token
        TOKEN_INFO['expires_at'] = time.time() + 3600
        return new_token
    else:
        print("Failed to refresh access token")
        return None

def get_valid_access_token():
    """Get a valid access token, refreshing if needed."""
    if not TOKEN_INFO['access_token'] or is_token_expired():
        return refresh_access_token()
    return TOKEN_INFO['access_token']

def fetch_events(query, token, variables):
    url = "https://api.meetup.com/gql"
    headers = {"Authorization": "Bearer " + token}
    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch events: {response.status_code} - {response.text}")
    return None

def extract_events(data, event_timeline):
    return data.get("data", {}).get("groupByUrlname", {}).get(event_timeline, {}).get("edges", [])

def update_events_cache(data):
    print('checking inside update_events_cache')
    event_type = data.get('event_type')
    group_name = data.get('group', {}).get('urlname')

    if event_type in ["event.created", "event.updated"] and group_name:
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

        variables = {"urlname": group_name}
        data = fetch_events(query, token, variables)

        if data:
            events = extract_events(data, "upcomingEvents")
            cache.set(f'events_{group_name}', events, timeout=86400)  # Cache for 24 hours

