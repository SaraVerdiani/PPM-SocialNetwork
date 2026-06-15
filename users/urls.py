
from django.urls import path, include
from .views import SignUpView, MyLoginView

app_name = 'users'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', MyLoginView.as_view(), name='login'),


]