from django.apps import AppConfig


# App configuration for the blog
# This is where we can customize app-wide settings and behaviors
class BlogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogs'
