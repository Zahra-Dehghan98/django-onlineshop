from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name ='signup'),
    path('login/', UserLoginView.as_view(), name ='login'),
    path('signup/', UserLogoutView.as_view(), name ='logout'),
    path('/', ShowAllProducts.as_view(), name='/'),
] 