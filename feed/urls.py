from django.urls import path

from feed.views import HomeView, ProfileView

app_name = 'feed'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
]