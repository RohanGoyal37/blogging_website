# Main URL Configuration for the entire website
# This is where we wire up our blog app and admin interface

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Main URL patterns for the website
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogs.urls')),
]

# In development, Django needs help serving uploaded files
# This sets up URLs for user-uploaded content
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
