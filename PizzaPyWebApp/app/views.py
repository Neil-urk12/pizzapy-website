from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#for Meetup
import requests
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from urllib.parse import urlparse


# Create your views here.

# @login_required
def index(request):
    context = {}
    return render(request, "index.html", context)

def event_page(request):
    return render(request, 'event_page.html')


def about_page(request):
    return render(request, 'about_page.html')

def get_redirect_uri(request):
    default_group_name = 'pizzapy-ph'
    current_location = request.build_absolute_uri()

    if current_location.startswith('http://127.0.0.1:8001/'):
        current_location = current_location.replace('http://127.0.0.1:8001/', 'https://pizzapy.ph/')

    parsed_url = urlparse(current_location)
    path = parsed_url.path.rstrip('/')
    parts = path.split('/')

    if len(parts) >= 3:
        if len(parts) == 3:  # URL is like /events/upcoming-events
            parts.append(default_group_name)  # Append default group name
        redirect_uri = '/'.join(parts)  # Join all parts to form the redirect URI
        return redirect_uri
    else:
        return None  # Unable to determine redirect URI



def get_access_token(request, code):
    REDIRECT_URI = get_redirect_uri(request)
    if not REDIRECT_URI:
        return None  # Unable to determine redirect URI
    
    token_url = 'https://secure.meetup.com/oauth2/access'
    payload = {
        'client_id': settings.OAUTH_KEY,
        'client_secret': settings.OAUTH_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': code
    }
    
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None

def fetch_events(query, token, variables):
    url = 'https://api.meetup.com/gql'
    headers = {"Authorization": "Bearer " + token}
    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def extract_events(data, event_timeline):
    return data.get("data", {}).get("groupByUrlname", {}).get(event_timeline, {}).get("edges", [])


def get_upcoming_events(request, group_name=None):
    if not group_name:
        group_name = "pizzapy-ph"
    upcoming_events_query = """
    query ($urlname: String!) {
        groupByUrlname(urlname: $urlname) {
            id,
            upcomingEvents(input: { first: 3 }, sortOrder: ASC){
                count,
                pageInfo {
                    endCursor
                },
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
    token = request.token
    if not token:
        return HttpResponse("Failed to retrieve access token", status=400)
    
    variables = {"urlname": group_name}
    data = fetch_events(upcoming_events_query, token, variables)
    
    if data:
        events = extract_events(data, "upcomingEvents")
        # print(events) 
        if events:
            first_event = events[0]["node"]
            other_events = [event["node"] for event in events[1:]]
            return render(request, 'event_page_test2.html', {'first_event': first_event, 'other_events': other_events})
        else:
            return HttpResponse("No upcoming events found", status=404)
    else:
        return HttpResponse("Failed to retrieve events", status=400)


def event_dispatcher(request, event_timeline, group_name=None):
    if event_timeline == 'past-events':
        return #get_past_events(request, group_name)
    elif event_timeline == 'upcoming-events':
        return get_upcoming_events(request, group_name)
    else:
        return HttpResponseNotFound("Event type not found")
    
    
def attend_event(request, event_id):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')  
        return HttpResponseRedirect(reverse('get_upcoming_events', args=[group_name]))
    else:
        return HttpResponse(status=405) 