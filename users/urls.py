
from django.urls import path, include
from . import views
from .views import SignUpView, MyLoginView

app_name = 'users'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', MyLoginView.as_view(redirect_authenticated_user=True), name='login'),

    path('logout/', views.logout_view, name='logout'),

]