from django.contrib import admin
from django.urls import path, include
from posts import views as posts_view
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', posts_view.home, name='home'),
    path('sign_up', posts_view.sign_up, name= 'sign_up'),
    path("login", posts_view.log_in, name='login'),
    path('posts/', include('posts.urls', namespace='posts')),
    path('captcha/', include('captcha.urls')),
 ]

if not settings.TESTING:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()