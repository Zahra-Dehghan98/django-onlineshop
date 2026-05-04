from django.contrib import admin
from .models import *

# Remove the "View Site" link from admin header
admin.site.site_url = None

"""Admin configuration for CustomerProfile model"""
@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']
#==================================================
"""Admin configuration for SellerProfile model"""
@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']
#==================================================
"""Admin configuration for Store model"""
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'description', 'location', 'rating']
#==================================================
"""Admin configuration for Product model"""
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'stock', 'image', 'store', 'created_at', 'rating']
#==================================================
"""Admin configuration for CartItem model"""
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'quantity']
#==================================================
"""Admin configuration for Order model"""
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'total_amount', 'date', 'status']
#==================================================
"""Admin configuration for OrderItem model"""
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
#==================================================
"""Admin configuration for Category model"""
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']