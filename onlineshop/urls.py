from django.urls import path
from .views import *

urlpatterns = [
    # Authentication URLs
    path('signup/', UserRegisterView.as_view(), name='signup'),           # User registration
    path('login/', UserLoginView.as_view(), name='login'),               # User login
    path('logout/', user_logout_view, name='logout'),                    # User logout
    
    # Product and Store browsing URLs
    path('', ShowAllProducts.as_view(), name='home'),                    # Home page - displays all products
    path('stores/', ShowAllStores.as_view(), name='stores'),             # List all stores
    path('stores/<int:pk>/', ShowDetailStore.as_view(), name='store_detail'),  # Store details
    
    # Seller panel URLs
    path('seller/', SellerPanelView.as_view(), name='seller_panel'),     # Seller dashboard
    path('seller/createstore/', AddStoreView.as_view(), name='create_store'),    # Create new store
    path('stores/<int:pk>/addproduct/', AddProductView.as_view(), name='add_product'),  # Add product to store
    path('stores/<int:pk>/editstore/', UpdateStoreView.as_view(), name='edit_store'),    # Edit store information
    
    # Customer panel URLs
    path('customer/', CustomerPanelView.as_view(), name='customer_panel'),     # Customer dashboard
    path('payment/', AddBalanceView.as_view(), name='payment'),           # Add balance to wallet
    
    # Shopping cart URLs
    path('cart/', AddedItemsListView.as_view(), name='cart'),             # View shopping cart
    path('stores/<int:store_id>/addtocart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),  # Add to cart
    path('cart/<int:item_id>/removefromcart/', RemoveFromCartView.as_view(), name='remove_from_cart'),     # Remove from cart
    
    # Checkout and order management
    path('checkout/', CheckoutView.as_view(), name='checkout'),           # Process checkout
    path('orderhistory/', OrderHistoryView.as_view(), name='order_history'),   # View order history
    path('thankyou/', ThankYouView, name='thank_you'),                    # Order confirmation page
    
    # Product management URLs
    path('editproduct/<int:pk>/', UpdateProductdetailView.as_view(), name='edit_product'),   # Edit product
    path('product/<int:pk>/', ShowDetailProduct.as_view(), name='product_detail'),           # Product details
]