from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserAccount
class RegisterForm(UserCreationForm):
    class Meta:
        model=UserAccount
        fields = ['email', 'type', 'password1','password2'] 