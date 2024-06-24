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

# REDIRECT_URI = 'https://pizzapy.ph/events/pizzapy-ph'
def get_redirect_uri(request):
    current_location = request.build_absolute_uri()
    parsed_url = urlparse(current_location)
    path = parsed_url.path.rstrip('/')  # Remove trailing slash if any
    parts = path.split('/')  # Split the path by "/"
    if len(parts) >= 3:  # Ensure that there are at least 3 parts
        return '/'.join(parts[:3])  # Join the first three parts
    else:
        return None  # Unable to determine the correct URI

# def get_access_token(code):
#     token_url = 'https://secure.meetup.com/oauth2/access'
#     payload = {
#         'client_id': settings.OAUTH_KEY,
#         'client_secret': settings.OAUTH_SECRET,
#         'grant_type': 'authorization_code',
#         'redirect_uri': REDIRECT_URI,
#         'code': code
#     }
#     response = requests.post(token_url, data=payload)
#     if response.status_code == 200:
#         return response.json().get('access_token')
#     else:
#         return None
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

def render_events(request, event_timeline, query, group_name):
    token = request.token
    if not token:
        return HttpResponse("Failed to retrieve access token", status=400)
    
    variables = {"urlname": group_name}
    data = fetch_events(query, token, variables)
    
    if data:
        events = extract_events(data, event_timeline)
        return render(request, 'events.html', {'events': events}) #@front-end, change the events.html to the desired template
    else:
        return HttpResponse("Failed to retrieve events", status=400)

def get_past_events(request, group_name=None):
    if not group_name:
        group_name = "pizzapy-ph"
    past_events_query = """
    query ($urlname: String!) {
        groupByUrlname(urlname: $urlname) {
            id
            pastEvents(input: { first: 3 }, sortOrder: DESC){
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
                                id
                                baseUrl
                                preview
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
    return render_events(request, "pastEvents", past_events_query, group_name)

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
                                id
                                baseUrl
                                preview
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
                        isAttending
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
        if events:
            first_event = events[0]["node"]
            other_events = [event["node"] for event in events[1:]]
            #@front-end, change the <file name>.html i.e. event_page_test.html
            return render(request, 'event_page_test.html', {'first_event': first_event, 'other_events': other_events}) 
        else:
            return HttpResponse("No upcoming events found", status=404)
    else:
        return HttpResponse("Failed to retrieve events", status=400)



# def get_upcoming_events(request, group_name):
#     upcoming_events_query = """
#     query ($urlname: String!) {
#         groupByUrlname(urlname: $urlname) {
#             id,
#             upcomingEvents(input: { first: 3 }, sortOrder: ASC){
#                 count,
#                 pageInfo {
#                     endCursor
#                     },
#                     edges {
#                     node {
#                         id
#                         title
#                         description
#                         eventType
#                         venue {
#                             address
#                             city
#                             postalCode
#                         }
#                         createdAt
#                         dateTime
#                         endTime
#                         timezone
#                         going
#                         shortUrl
#                         isAttending
#                         rsvpState
#                         host {
#                             name
#                             username
#                             email
#                             memberPhoto {
#                                 id
#                                 baseUrl
#                                 preview
#                                 source
#                             }
#                             memberUrl
#                             organizedGroupCount
#                         }

#                     }
#                 }
#             }
#         }
#         }
#     """
#     return render_events(request, "upcomingEvents", upcoming_events_query, group_name)



def event_dispatcher(request, event_timeline, group_name=None):
    if event_timeline == 'past-events':
        return get_past_events(request, group_name)
    elif event_timeline == 'upcoming-events':
        return get_upcoming_events(request, group_name)
    else:
        return HttpResponseNotFound("Event type not found")
    
    
def attend_event(request, event_id):
    if request.method == 'POST':
        # Handle the logic to mark the event as attended by the user
        # This might involve calling an API or updating your database
        # For example:
        # user = request.user
        # mark_event_as_attended(user, event_id)
        
        # Redirect back to the upcoming events page
        group_name = request.POST.get('group_name')  # Make sure to pass the group_name in the form
        return HttpResponseRedirect(reverse('get_upcoming_events', args=[group_name]))
    else:
        return HttpResponse(status=405)  # Method Not Allowed

def join_group(request, event_id):
    if request.method == 'POST':
        # Handle the logic to join the group before attending the event
        # This might involve calling an API or updating your database
        # For example:
        # user = request.user
        # join_group_for_event(user, event_id)
        
        # Redirect back to the upcoming events page
        group_name = request.POST.get('group_name')  # Make sure to pass the group_name in the form
        return HttpResponseRedirect(reverse('get_upcoming_events', args=[group_name]))
    else:
        return HttpResponse(status=405)  # Method Not Allowed