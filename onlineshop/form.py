from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'password1', 'password2', 'is_seller']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=11)
    password = forms.CharField(max_length=50)

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'stock']

class AddStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'location']

