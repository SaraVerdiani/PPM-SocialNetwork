from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
    path('createpost/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
]