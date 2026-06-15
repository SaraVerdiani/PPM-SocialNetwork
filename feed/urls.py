from django.urls import path

from feed.views import HomeView

app_name = 'feed'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
]