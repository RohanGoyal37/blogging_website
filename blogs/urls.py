# URL configuration for the blog app
# Maps URLs to their corresponding view functions

from django.urls import path
from django.contrib.auth import views as auth_views  # Django's built-in auth views
from . import views

# List of URL patterns - Django matches URLs from top to bottom
urlpatterns = [
    path('', views.public_home, name='public_home'),
    path('home/', views.index, name='index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blogs/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('search/', views.search_posts, name='search_posts'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', views.my_bookmarks, name='my_bookmarks'),
]
