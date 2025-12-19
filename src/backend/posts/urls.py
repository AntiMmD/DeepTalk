from django.urls import path
from posts import views

app_name = "posts"

urlpatterns = [
    # CSRF and auth
    path("api/csrf/", views.csrf_token_view, name="api_csrf"),
    path("api/login/", views.api_login, name="api_login"),
    path("api/signup/", views.api_signup, name="api_signup"),
    path("api/logout/", views.api_logout, name="api_logout"),

    # posts API
    path("api/posts/", views.posts_api_list, name="api_posts_list"),
    path("api/posts/create", views.posts_api_create, name="api_posts_create"),
    path("api/posts/<int:id>/edit", views.posts_api_edit, name="api_posts_edit"),
    path("api/posts/<int:id>/delete", views.posts_api_delete, name="api_posts_delete"),
]
