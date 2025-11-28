from django.urls import path
from posts import views

app_name = 'posts' 

urlpatterns = [
    path('new', views.create_post, name='create_post'),
    path('posted/<int:id>/delete', views.delete_post, name='delete_post'),
    path('posted/<int:id>/edit', views.edit_post, name='edit_post'),
    path('posted/<int:id>', views.post_view, name= 'post_view'),
    path('posted', views.post_manager, name='post_manager'),
 ]

