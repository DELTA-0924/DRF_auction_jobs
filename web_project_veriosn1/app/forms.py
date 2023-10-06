from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1')
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2',
                  'fio', 'location', 'skills', 'salary', 
                  'about', 'year', 'speciality', 'avatar')

  