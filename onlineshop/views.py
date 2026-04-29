from .form import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import View
from django.db import transaction

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        is_seller = form.cleaned_data.get('is_seller',False)
        if is_seller:
            SellerProfile.objects.create(user = user)
            messages.success(self.request, f'Seller account created for {user.last_name}')
        else:
            CustomerProfile.objects.create(user=user)
            messages.success(self.request, f'Customer account created for {user.last_name}')
        login(self.request, user) 
        return response  
    
    def form_invalid(self, form):
        messages.error(self.request, 'Registration failed. Please try again')
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
            return reverse_lazy('seller_panel') 
        else:
            return reverse_lazy('customer_panel') 

    def form_invalid(self, form):
        messages.error(self.request, 'Incorrect phone number or password')
        return super().form_invalid(form)

def user_logout_view(request):
    logout(request)
    return render(request, 'logged_out.html')
#===================================================================
class ShowAllProducts(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        cat_id = self.request.GET.get('cat')
        if cat_id:
            queryset = queryset.filter(category_id=cat_id)
    
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q.lower())
        return queryset
#============================================
class ShowAllStores(ListView):
    model = Store
    template_name = 'stores.html'
    context_object_name = 'stores'
#===================================================================
class ShowDetailStore(DetailView):
    model = Store
    template_name = 'store_detail.html'
    context_object_name = 'store'
#===================================================
class SellerPanelView(LoginRequiredMixin, ListView):
    model = Store
    template_name = 'seller_panel.html'
    context_object_name = 'stores'

    def get_queryset(self):
        user = self.request.user
        try:
            seller_profile_instance = user.sellerprof
            return Store.objects.filter(seller=seller_profile_instance)
        except SellerProfile.DoesNotExist:
            return Store.objects.none()       
#===================================================
class AddStoreView(CreateView):
    model = Store
    form_class = AddStoreForm
    template_name = 'create_store.html'
    context_object_name = 'store'
    success_url = reverse_lazy ('stores')

    def form_valid(self, form):
        seller_profile = SellerProfile.objects.get(user=self.request.user)
        form.instance.seller = seller_profile
        return super().form_valid(form)
#===================================================
class AddProductView(CreateView):
    model = Product
    form_class = AddProductForm
    template_name = 'create_product.html'
    success_url = reverse_lazy ('home')
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        
        store_id = self.kwargs.get('pk') 
        store = get_object_or_404(Store, pk=store_id)
        
        obj.store = store
        obj.save()
        return super().form_valid(form)
#===================================================
class CustomerPanelView(LoginRequiredMixin, DetailView):
    model = CustomerProfile
    template_name = 'customer_panel.html'
    context_object_name = 'customer_profile'

    def get_object(self):
        user = self.request.user
        if user.is_seller == True:
            messages.error(self.request, "")
        else:
            customer = CustomerProfile.objects.get(user=user)
            return customer  
#===================================================
class AddedItemsListView(ListView):
    model = CartItem
    template_name = 'cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        user = self.request.user 
        if not user.is_authenticated:
            return CartItem.objects.none()
        try:
            customer = CustomerProfile.objects.get(user=user)
            return CartItem.objects.filter(customer=customer)
        except CustomerProfile.DoesNotExist:
            return CartItem.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = 0
        for item in context['cart_items']:
            total += item.product.price * item.quantity
        context['total'] = total
        return context
#===================================================
class AddToCartView(View):
    def post(self, request, store_id, product_id):
        product = get_object_or_404(Product, pk=product_id)
        store = get_object_or_404(Store, pk=store_id)
        try:
            customer = request.user.customerprof
        except AttributeError:
            messages.error(request, "Customer profile not found")
            return redirect('store_detail', pk=store_id)
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity <= 0:
                raise ValueError("Product quantity must be a positive number")
            if product.stock < quantity:
                messages.error(request, "Not enough product in stock")
                return redirect('store_detail', pk=store_id)     
        except (ValueError, TypeError):
            messages.error(request, "Quantity value is invalid")
            return redirect('store_detail', pk=store_id)
        
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            customer=customer,
            defaults={'quantity': quantity} 
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.save()

        product.stock -= quantity
        product.save()
        
        messages.success(request, "Product added to cart successfully")
        return redirect('cart')
#======================================================
class RemoveFromCartView(View):
    model = CartItem
    template_name = 'cart.html'
    
    def get(self, request, item_id):
        item = CartItem.objects.get(id = item_id)
        product = item.product
        product.stock += item.quantity
        product.save()
        item.delete()
        item2 = CartItem.objects.all()
        return render (request, 'cart.html', {'cart_items':item2})
#======================================================
class AddBalanceView(View):
    def get(self, request):
        return render (request, 'payment.html')

    def post(self, request):
        user = self.request.user
        amount = int(request.POST.get('amount', 0))
        customer_profile = CustomerProfile.objects.get(user=user)
        customer_profile.balance += amount
        customer_profile.save()
        return redirect('thank_you')
#=======================================================
class CheckoutView(View):
    @transaction.atomic
    def post(self, request):
        user = request.user
        customer = CustomerProfile.objects.get(user = user)
        cart_items = CartItem.objects.filter(customer=customer)
        if not cart_items.exists(): 
            messages.error(request, "your cart is empty!")
            return redirect('cart')
        total = 0
        for item in cart_items:
            total += item.product.price * item.quantity
            if customer.balance < total:
                messages.info(request, "Your wallet balance is less than the cart total.")
                return redirect ('payment')
        customer.balance -= total
        customer.save()
        for item in cart_items:
            seller = item.product.store.seller
            amount = item.product.price * item.quantity
            seller.balance += amount
            seller.save()
        order = Order.objects.create(customer=customer, total_amount = total)
        for item in cart_items:
            order_item = OrderItem.objects.create(order= order, product = item.product, quantity = item.quantity, price = item.product.price)
        cart_items.delete()
        return redirect ('thank_you')
#=================================================  
class OrderHistoryView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order_history.html'

    def get_queryset(self):
        user = self.request.user
        try:
            customer = CustomerProfile.objects.get(user=user)
            return Order.objects.filter(customer=customer)
        except CustomerProfile.DoesNotExist:
            return Order.objects.none()
#====================================================
def ThankYouView(request):
    return render(request, 'thank_you.html')













        
            




    

        