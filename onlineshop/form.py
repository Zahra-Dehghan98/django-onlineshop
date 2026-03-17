from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=11)
    is_seller = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'password1', 'password2', 'is_seller']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=11)
    password = forms.CharField(max_length=50)