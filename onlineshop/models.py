from django.contrib.auth.models import User
from django.db import models

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name='مشتری')
    phone = models.CharField(max_length=11, unique=True, blank=False, null=False, verbose_name='شماره تماس', editable=True)
    balance = models.PositiveIntegerField(default=0, verbose_name='موجودی کیف پول' ,editable=True)

    class Meta:
        verbose_name = ' پروفایل مشتری'
        verbose_name_plural = 'پروفایل های مشتری'
        ordering = ['created_at']

    def __str__(self):
        return self.user.username
    
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name='فروشنده')
    phone = models.CharField(max_length=11, unique=True, blank=False, null=False, verbose_name='شماره تماس', editable=True)
   

    class Meta:
        verbose_name = 'پروفایل فروشنده'
        verbose_name_plural = 'پروفایل فروشنده ها'
        ordering = ['created_at']

    def __str__(self):
        return self.user.username
    

class Store(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False, verbose_name='فروشگاه')
    seller = models.ForeignKey(SellerProfile, on_delete = models.CASCADE, verbose_name='فروشنده')
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name='اطلاعات تماس', editable=True)
    location = models.CharField(max_length=50, blank=True, null=True, verbose_name='مکان', editable=True)
    rating = models.DecimalField(max_digits=5, decimal_places =1, blank=True, null=True, editable=True)
    

    class Meta:
        verbose_name = 'فروشگاه'
        verbose_name_plural = 'فروشگاه ها'
        ordering = ['created_at']

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False, verbose_name='نام کالا')
    balance = models.PositiveIntegerField(blank=False, null=False, verbose_name='قیمت', editable=True)
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name='اطلاعات محصول')
    image = models.ImageField(upload_to='productpic/', blank=False, null=False, verbose_name='تصویر محصول', editable=True)
    store = models.ForeignKey(Store, on_delete = models.CASCADE, verbose_name='فروشگاه')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=5, decimal_places =1, blank=True, null=True, editable=True)
    

    class Meta:
        verbose_name = 'فروشگاه'
        verbose_name_plural = 'فروشگاه ها'
        ordering = ['created_at']

    def __str__(self):
        return self.name
    







