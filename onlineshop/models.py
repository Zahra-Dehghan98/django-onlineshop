from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, password=None, **extra_fileds):
        first_name = extra_fileds.get('first_name')
        last_name = extra_fileds.get('last_name')
        if not phone:
            raise ValueError("The phone field must be set")
        if not first_name or not last_name:
            raise ValueError("the fullname must be set")
        user = self.model(phone=phone, **extra_fileds)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(phone, password,**extra_fields)
    
    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_active') is not True:
            raise ValueError('superuser must have is_active = True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser = True')
        
        return self._create_user(phone, password,**extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True, verbose_name='phone number')
    first_name = models.CharField(max_length=50, verbose_name='first name')
    last_name = models.CharField(max_length=50, verbose_name='last name')
    is_seller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects= CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='customerprof', verbose_name='customer')
    balance = models.PositiveIntegerField(default=0, verbose_name='balance' ,editable=True)

    class Meta:
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customer Profiles'
        ordering = ['user']

    def __str__(self):
        return self.user.first_name
    
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='sellerprof', verbose_name='seller')
    balance = models.PositiveIntegerField(default=0, verbose_name='balance' ,editable=True)

    class Meta:
        verbose_name = 'Seller Profile'
        verbose_name_plural = 'Seller Profiles'
        ordering = ['user']

    def __str__(self):
        return self.user.first_name
    

class Store(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False, verbose_name='store')
    seller = models.ForeignKey(SellerProfile, on_delete = models.CASCADE, related_name='store', verbose_name='seller')
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name='description', editable=True)
    location = models.CharField(max_length=50, blank=True, null=True, verbose_name='location', editable=True)
    rating = models.DecimalField(max_digits=5, decimal_places =1, blank=True, null=True, verbose_name='rate')
    

    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='category name', unique=True)
    slug = models.SlugField(max_length=200, unique=True, verbose_name='slug')
    
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False, verbose_name='product')
    price = models.PositiveIntegerField(blank=False, null=False, verbose_name='price', editable=True)
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name='description of the product')
    stock = models.IntegerField(default=1, verbose_name='stock')
    image = models.ImageField(upload_to='productpic/', blank=False, null=False, verbose_name='image of the product', editable=True)
    store = models.ForeignKey(Store, on_delete = models.CASCADE, related_name='product', verbose_name='store')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=5, decimal_places =1, blank=True, null=True, verbose_name='rate')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='category')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='cartitem', verbose_name='customer')
    quantity = models.PositiveIntegerField(default=1 ,verbose_name='quantity')
    
    class Meta:
        verbose_name = 'CartItem'
        ordering = ['customer']
        unique_together = ('customer', 'product')

    def __str__(self):
        return f'quantity:{self.quantity} - product: {self.product} in CartItem of {self.customer}'

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', _('در انتظار')
        PROCESSING = 'processing', _('در حال پردازش')
        SHIPPED = 'shipped', _('ارسال شده')
        DELIVERED = 'delivered', _('تحویل شده')
        CANCELLED = 'cancelled', _('لغو شده')
        RETURNED = 'returned', _('مرجوع شده')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='order', verbose_name='customer')
    total_amount = models.PositiveIntegerField(verbose_name='total amount')
    date = models.DateTimeField(auto_now_add=True, verbose_name='date of the order')
    status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.PENDING, verbose_name='status', editable=True)
    

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-date']

    def __str__(self):
        return f'order: {self.customer} in date:{self.date} - total amount: {self.total_amount} in status:{self.status}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem', verbose_name='order')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='product')
    quantity = models.PositiveIntegerField(default=1 ,verbose_name='quntity')
    price = models.PositiveIntegerField(verbose_name='price', editable= False)

    class Meta:
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems'
        unique_together = ('order', 'product')
        ordering = ['order']


