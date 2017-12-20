from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView


class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/user_registration.html'
    
    def get_success_url(self):
        return reverse('home')
