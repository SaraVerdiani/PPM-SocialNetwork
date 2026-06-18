from django.urls import path

from feed import views
from feed.views import HomeView, ExploreView

app_name = 'feed'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('explore/', ExploreView.as_view(), name='explore'),
]