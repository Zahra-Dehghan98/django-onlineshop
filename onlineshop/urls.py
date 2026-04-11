from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name ='signup'),
    path('login/', UserLoginView.as_view(), name ='login'),
    path('logout/', user_logout_view, name ='logout'),
    path('/', ShowAllProducts.as_view(), name='/'),
    path('stores/', ShowAllStores.as_view(), name='stores'),
    path('stores/<int:pk>/', ShowDetailStore.as_view(), name='store_detail'),
    path('seller/', SellerPanelView.as_view(), name='seller_panel'),
    path('seller/createstore/', AddStoreView.as_view(), name='create_store'),
    path('stores/<int:pk>/addproduct/', AddProductView.as_view(), name='add_product'),
] 