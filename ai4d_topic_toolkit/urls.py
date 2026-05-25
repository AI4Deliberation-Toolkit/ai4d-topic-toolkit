"""URL configuration for ai4d_topic_toolkit project."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('topic_extraction.urls')),
]
