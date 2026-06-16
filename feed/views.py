from django.views.generic import TemplateView

class HomeView(TemplateView):
    
    template_name = 'sitecontent/home.html'

class ProfileView(TemplateView):
    template_name = 'users/profile.html'