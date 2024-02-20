from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=20, required=False, help_text='Required. Enter your username.')
    email = forms.CharField(max_length=20, required=False, help_text='Required. Enter your username.')
    password1 = forms.CharField(max_length=20, required=False, help_text='Required. Enter your username.')
    password2 = forms.CharField(max_length=20, required=False, help_text='Required. Enter your username.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']