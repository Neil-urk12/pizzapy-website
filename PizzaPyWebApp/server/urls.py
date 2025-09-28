"""
URL configuration for PizzaPyWebApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from app import views

urlpatterns = [
    # HOME PAGE
    path("", views.index, name="index"),
    # EVENT PAGE
    path("events/", views.event_page, name="events"),
    # ABOUT US PAGE
    path("about_us/", views.about_page, name="about_page"),
    # EVENTS
    # event_timeline = upcoming-events
    # path('events/', views.event_dispatcher, name='events'),
    # FOR JACOB's EVENTS
    # group_name = meetup group name e.g. pizzapy-ph
    # SAMPLE: events/upcoming-events/cebu-city-cybersecurity-center-c4
    # path('events/<str:event_timeline>/<str:group_name>/', views.event_dispatcher, name='events'),
    # path('attend_event/<int:event_id>/', views.attend_event, name='attend_event'),
path('discord/', RedirectView.as_view(url='https://discord.gg/nt9grSKsWN', permanent=False), name='discord'),
    path('facebook/', RedirectView.as_view(url='https://www.facebook.com/groups/pizzapy.ph/', permanent=False), name='facebook'),
    path('github/', RedirectView.as_view(url='https://github.com/pizzapy/', permanent=False), name='github'),
    path('linkedin/', RedirectView.as_view(url='https://www.linkedin.com/company/pizzapy-ph/', permanent=False), name='linkedin'),
    path('meetup/', RedirectView.as_view(url='https://www.meetup.com/pizzapy-ph/', permanent=False), name='meetup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        "/images/", document_root=os.path.join(settings.BASE_DIR, "static/images")
    )
