from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *

"""Form for user registration including seller/customer role selection"""
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'password1', 'password2', 'is_seller']
#================================================
"""Custom login form using phone number instead of username"""
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=11)
    password = forms.CharField(max_length=50)
#================================================
"""Form for sellers to add new products to their store"""
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'image', 'stock']
#================================================
"""Form for sellers to create a new store"""
class AddStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'location']

