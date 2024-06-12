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
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("main/", include("app.urls")),
    path("", views.index, name="index"),
    path('events/', views.event_page, name='events'),
    path('events/<str:group_name>/', views.get_past_events, name='events'), #display past events depends on the group name e.g http://127.0.0.1:8000/events/pizzapy-ph/
    path('events/<str:group_name>/', views.get_upcoming_events, name='events'), #display past events depends on the group name e.g http://127.0.0.1:8000/events/pizzapy-ph/
    path('about_us/', views.about_page, name='about_page'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static('/images/', document_root=os.path.join(settings.BASE_DIR, 'static/images'))