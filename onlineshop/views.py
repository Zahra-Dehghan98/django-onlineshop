from .form import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView
from .models import *
class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        is_seller = form.cleaned_data.get('is_seller',False)
        if is_seller:
            SellerProfile.objects.create(user = user)
            messages.success(self.request, f'user:{user.last_name} created as a seller')
        else:
            CustomerProfile.objects.create(user=user)
            messages.success(self.request, f'user:{user.last_name} created as a customer')
        login(self.request, user) 
        return response  
    
    def form_invalid(self, form):
        messages.error(self.request, 'the register is not successfully')
        return super().form_invalid(form)
    
class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        response = super().form_valid(form)  
        user = form.get_user()
        if user.is_seller:
            messages.success(self.request, f'{user.last_name} logged in as seller')
        else:
            messages.success(self.request, f'{user.last_name} logged in as customer')
        return response

    def get_success_url(self):
        user = self.request.user
        if user.is_seller:
            return reverse_lazy('signup') 
        else:
            return reverse_lazy('signup') 

    def form_invalid(self, form):
        messages.error(self.request, 'the username or password in not correct')
        return super().form_invalid(form)

class UserLogoutView(LogoutView):
    template_name = 'logged_out.html'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'the user id logged out successfully')
        return super().dispatch(request, *args, **kwargs)
    
#===================================================================
class ShowAllProducts(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'product'
