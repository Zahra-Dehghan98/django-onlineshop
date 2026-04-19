from django.contrib import admin
from .models import *

admin.site.site_url = None

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'description', 'location', 'rating']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'stock', 'image', 'store', 'created_at', 'rating']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer','total_amount', 'date', 'status']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product', 'quantity', 'price']





