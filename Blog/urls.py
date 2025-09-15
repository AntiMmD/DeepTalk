from django.contrib import admin
from django.urls import path
from posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('posts/new', views.post_form, name='post_form'),
    path('posts/posted/<int:id>', views.post_view, name= 'post_view'),
]

