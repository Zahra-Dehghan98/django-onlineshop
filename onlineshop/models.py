from django.contrib.auth.models import User
from django.db import models

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='customerprof', verbose_name='مشتری')
    phone = models.CharField(max_length=11, unique=True, verbose_name='شماره تماس', editable=True)
    first_name = models.CharField(max_length=50,blank=True, null=True, verbose_name='نام', editable=True)
    last_name = models.CharField(max_length=60,blank=True, null=True, verbose_name='نام خوانوادگی', editable=True)
    balance = models.PositiveIntegerField(default=0, verbose_name='موجودی کیف پول' ,editable=True)

    class Meta:
        verbose_name = ' پروفایل مشتری'
        verbose_name_plural = 'پروفایل های مشتری'
        ordering = ['first_name']

    def __str__(self):
        return self.user.username
    
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='sellerprof', verbose_name='فروشنده')
    phone = models.CharField(max_length=11, unique=True, verbose_name='شماره تماس', editable=True)
    first_name = models.CharField(max_length=50,blank=True, null=True, verbose_name='نام', editable=True)
    last_name = models.CharField(max_length=60,blank=True, null=True, verbose_name='نام خوانوادگی', editable=True)
   

    class Meta:
        verbose_name = 'پروفایل فروشنده'
        verbose_name_plural = 'پروفایل فروشنده ها'
        ordering = ['first_name']

    def __str__(self):
        return self.user.username
    

class Store(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False, verbose_name='فروشگاه')
    seller = models.ForeignKey(SellerProfile, on_delete = models.CASCADE, related_name='store', verbose_name='فروشنده')
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name='اطلاعات تماس', editable=True)
    location = models.CharField(max_length=50, blank=True, null=True, verbose_name='مکان', editable=True)
    rating = models.DecimalField(max_digits=5, decimal_places =1, blank=True, null=True, editable=True, verbose_name='امتیاز')
    

    class Meta:
        verbose_name = 'فروشگاه'
        verbose_name_plural = 'فروشگاه ها'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False, verbose_name='نام کالا')
    price = models.PositiveIntegerField(blank=False, null=False, verbose_name='قیمت', editable=True)
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name='اطلاعات محصول')
    image = models.ImageField(upload_to='productpic/', blank=False, null=False, verbose_name='تصویر محصول', editable=True)
    store = models.ForeignKey(Store, on_delete = models.CASCADE,related_name='product', verbose_name='فروشگاه')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=5, decimal_places =1, blank=True, null=True, editable=True, verbose_name='امتیاز')
    

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['created_at']

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='نام محصول')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='cartitem', verbose_name='مشتری')
    quantity = models.PositiveIntegerField(default=1 ,verbose_name='تعداد محصول')
    
    class Meta:
        verbose_name = 'سبد خرید'
        ordering = ['customer']
        unique_together = ('customer', 'product')

    def __str__(self):
        return f'تعداد {self.quantity} - محصول{self.product} در سبد خرید {self.customer}'

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', ('در انتظار')
        PROCESSING = 'processing', ('در حال پردازش')
        SHIPPED = 'shipped', ('ارسال شده')
        DELIVERED = 'delivered', ('تحویل شده')
        CANCELLED = 'cancelled', ('لغو شده')
        RETURNED = 'returned', ('مرجوع شده')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='order', verbose_name='مشتری')
    total_amount = models.PositiveIntegerField(verbose_name='مبلغ کل')
    date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ سفارش')
    status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.PENDING, verbose_name='وضعیت سفارش')
    

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'
        ordering = ['date']

    def __str__(self):
        return f'سفارش {self.customer}در تاریخ {self.date} به مبلغ {self.total_amount}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='نام محصول')
    quantity = models.PositiveIntegerField(default=1 ,verbose_name='تعداد محصول')
    price = models.PositiveIntegerField(verbose_name='قیمت')


    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم های سفارش'
        unique_together = ('order', 'product')
        ordering = ['order']

    







