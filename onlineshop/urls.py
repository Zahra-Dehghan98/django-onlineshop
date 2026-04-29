from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name ='signup'),
    path('login/', UserLoginView.as_view(), name ='login'),
    path('logout/', user_logout_view, name ='logout'),
    path('', ShowAllProducts.as_view(), name='home'),
    path('stores/', ShowAllStores.as_view(), name='stores'),
    path('stores/<int:pk>/', ShowDetailStore.as_view(), name='store_detail'),
    path('seller/', SellerPanelView.as_view(), name='seller_panel'),
    path('seller/createstore/', AddStoreView.as_view(), name='create_store'),
    path('stores/<int:pk>/addproduct/', AddProductView.as_view(), name='add_product'),
    path('customer/', CustomerPanelView.as_view(), name='customer_panel'),
    path('cart/', AddedItemsListView.as_view(), name='cart'),
    path('stores/<int:store_id>/addtocart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/<int:item_id>/removefromcart/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('payment/', AddBalanceView.as_view(), name='payment'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orderhistory/', OrderHistoryView.as_view(), name='order_history'),
    path('thankyou/', ThankYouView, name='thank_you'),
    path('editproduct/<int:pk>/', UpdateProductdetailView.as_view(), name='edit_product'),
    path('stores/<int:pk>/editstore/', UpdateStoreView.as_view(), name='edit_store')
] 