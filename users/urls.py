
from django.urls import path, include
import feed
from . import views
from .views import SignUpView, MyLoginView
from feed.views import profile_view

app_name = 'users'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', MyLoginView.as_view(redirect_authenticated_user=True), name='login'),

    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', feed.views.profile_view, name='profile'),
    path('profile/<str:username>/follow/', views.follow, name='follow'),
    path('profile/edit/pin-post/', views.choose_pinned_post, name='choose_pinned_post'),
    path('requests/', views.follow_requests, name='follow_requests'),
    path('requests/<int:follow_id>/accept/', views.accept_request, name='accept_request'),
    path('requests/<int:follow_id>/reject/', views.reject_request, name='reject_request'),

    path('profile/<str:username>/followers/', views.follow_list, {'follow_type': 'followers'}, name='followers'),
    path('profile/<str:username>/following/', views.follow_list, {'follow_type': 'following'}, name='following'),
    path('profile/<str:username>/ban', views.ban_user, name='ban_user'),


]