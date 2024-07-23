from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseBadRequest,
)
from django.urls import reverse
from django.conf import settings
from urllib.parse import urlparse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import *
import jwt
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


# Create your views here.

# NAV LINK (PAGES)
def index(request):
    context = {}
    return render(request, "index.html", context)


def event_page(request, group_name=None):
    # return render(request, 'event_page.html')
    return get_upcoming_events(request, group_name)


def about_page(request):
    return render(request, "about_page.html")


# GET ALL UPCOMING EVENTS API
# def get_upcoming_events(request, group_name=None):
#     if not group_name:
#         group_name = "pizzapy-ph"

#     # Try to get events from cache
#     events = cache.get(f'events_{group_name}')
    
#     if not events:
#         # Cache miss, fetch from Meetup API
#         upcoming_events_query = """
#         query ($urlname: String!) {
#             groupByUrlname(urlname: $urlname) {
#                 id,
#                 upcomingEvents(input: { first: 3 }, sortOrder: ASC){
#                     count,
#                     pageInfo {
#                         endCursor
#                     },
#                     edges {
#                         node {
#                             id
#                             title
#                             description
#                             eventType
#                             images {
#                                 source
#                             }
#                             venue {
#                                 address
#                                 city
#                                 postalCode
#                             }
#                             createdAt
#                             dateTime
#                             endTime
#                             timezone
#                             going
#                             shortUrl
#                             host {
#                                 name
#                                 username
#                                 email
#                                 memberPhoto {
#                                     id
#                                     baseUrl
#                                     preview
#                                     source
#                                 }
#                                 memberUrl
#                                 organizedGroupCount
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#         """

#         token = get_valid_access_token()
#         if not token:
#             return HttpResponse("Failed to retrieve access token", status=400)

#         variables = {"urlname": group_name}
#         data = fetch_events(upcoming_events_query, token, variables)

#         if data:
#             events = extract_events(data, "upcomingEvents")
#             cache.set(f'events_{group_name}', events, timeout=86400)  # Cache for 24 hours
#         else:
#             events = []

#     if events:
#         first_event = events[0]["node"] if len(events) > 0 else None
#         other_events = [event["node"] for event in events[1:]]
#         return render(
#             request,
#             "event_page.html",
#             {"first_event": first_event, "other_events": other_events},
#         )
#     else:
#         return render(
#             request,
#             "event_page.html",
#             {"error_message": "No upcoming events found", "events_json": "[]"},
#         )

def get_upcoming_events(request, group_name=None):
    if not group_name:
        group_name = "pizzapy-ph"

    # Try to get events from cache
    events = cache.get(f'events_{group_name}')

    if not events:
        return render(
            request,
            "event_page.html",
            {"error_message": "No upcoming events found", "events_json": "[]"},
        )

    first_event = events[0]["node"] if len(events) > 0 else None
    other_events = [event["node"] for event in events[1:]]
    return render(
        request,
        "event_page.html",
        {"first_event": first_event, "other_events": other_events},
    )


# @csrf_exempt
# def meetup_webhook(request):
#     if request.method == 'POST':

#         try:
#             data = json.loads(request.body)
#             print(data)
#             # Process the webhook data
#             update_events_cache(data)
#             return JsonResponse({'status': 'success'})
#         except json.JSONDecodeError:
#             return HttpResponseBadRequest("Invalid JSON")
#     return HttpResponseBadRequest("Invalid request method")

#CHECKING CACHE
def check_cache(request):
    group_names = [
        "pizzapy-ph",
        "cebu-city-cybersecurity-center-c4",
        "p5-management-hub",
    ]

    cached_data = {}
    for group_name in group_names:
        cached_events = cache.get(f'events_{group_name}')
        cached_data[group_name] = cached_events

    return JsonResponse(cached_data)