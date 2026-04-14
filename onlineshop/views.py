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

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'signup.html'
    success_url = reverse_lazy('/')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        is_seller = form.cleaned_data.get('is_seller',False)
        if is_seller:
            SellerProfile.objects.create(user = user)
            messages.success(self.request, f'user:{user.last_name} created as a seller')
        else:
            CustomerProfile.objects.create(user=user)
            messages.success(self.request, f'user:{user.last_name} created as a customer')
        login(self.request, user) 
        return response  
    
    def form_invalid(self, form):
        messages.error(self.request, 'the register is not successfully')
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
            return reverse_lazy('signup') 

    def form_invalid(self, form):
        messages.error(self.request, 'the username or password in not correct')
        return super().form_invalid(form)

def user_logout_view(request):
    logout(request)
    return render(request, 'logged_out.html')
    
#===================================================================
class ShowAllProducts(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
#===================================================================
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
    context_object_name = 'store'

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
    success_url = reverse_lazy ('/')


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
        customer = CustomerProfile.objects.get(user=user)
        return customer  
#===================================================
class AddedItemsListView(ListView):
    model = CartItem
    template_name = 'cart.html'
    context_object_name = 'cart_items'
#===================================================
class AddToCartView(View):
    def post(self, request, store_id, product_id):
        product = get_object_or_404(Product, pk=product_id)
        store = get_object_or_404(Store, pk=store_id)
        try:
            customer = request.user.customerprof
        except AttributeError:
            messages.error(request, "پروفایل مشتری یافت نشد.")
            return redirect('store_detail', pk=store_id)
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity <= 0:
                raise ValueError("تعداد باید مثبت باشد")
            if product.stock < quantity:
                messages.error(request, "موجودی محصول کافی نیست.")
                return redirect('store_detail', pk=store_id)     
        except (ValueError, TypeError):
            messages.error(request, "تعداد نامعتبر است.")
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
        
        messages.success(request, "محصول با موفقیت به سبد خرید اضافه شد.")
        return redirect('store_detail', pk=store_id)
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

        