from django.urls import path
from posts import views

app_name = 'posts' 

urlpatterns = [
    path('new', views.post_form, name='post_form'),
    path('posted/<int:id>', views.post_view, name= 'post_view'),
    path('posted', views.post_manager, name='post_manager'),
    path('posted/<int:id>/delete', views.delete_post, name='delete_post')
 ]

