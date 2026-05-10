# 🛍️ Kaleido - Online Store

An e-commerce platform built with Django featuring customer and seller roles.

---

## ✨ Features

### 👥 User Roles
- **Customer** – Purchase, cart, wallet, order history
- **Seller** – Create store, manage products
- **Admin** – Django admin panel (no front-end access)

### 🛒 Main Features
- Product search and category filtering
- Shopping cart with quantity management
- Virtual wallet system
- Checkout with balance validation
- Product image upload

### 🎨 Frontend
- Responsive design (mobile, tablet, laptop)
- Modern and clean UI

---

## 🛠️ Tech Stack

- Django 6.0, Python 3.14
- PostgreSQL
- HTML5, CSS3

---

## 🚀 Quick Installation

```bash```

git clone git clone https://github.com/Zahra-Dehghan98/django-onlineshop.git

cd (project directory)

python -m venv venv

source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate --settings=config.settings.dev

python manage.py createsuperuser --settings=config.settings.dev

python manage.py runserver --settings=config.settings.dev


---

📍 **URLs**

/onlineshop/              → Home page

/onlineshop/signup/       → User registration

/onlineshop/login/        → User login

/onlineshop/logout/       → User logout

/onlineshop/stores/       → List all stores

/onlineshop/stores/<id>/  → Store details

/onlineshop/cart/         → Shopping cart

/onlineshop/checkout/     → Checkout

/onlineshop/orderhistory/ → Order history

/onlineshop/payment/      → Add wallet balance

/onlineshop/thankyou/     → Thank you page

/onlineshop/seller/       → Seller panel

/onlineshop/customer/     → Customer panel

/onlineshop/seller/createstore/ → Create store

/onlineshop/stores/<id>/addproduct/ → Add product

/onlineshop/editproduct/<id>/ → Edit product

/onlineshop/stores/<id>/editstore/ → Edit store

/onlineshop/product/<id>/ → Product details

/admin/                   → Admin panel

---

👥 **Roles**

🛍️ **CUSTOMER**
→ Browse products
→ Add to cart
→ Checkout
→ Wallet recharge
→ Order history

🏪 **SELLER**
→ Create store
→ Add / edit products
→ View earnings

👑 **SUPERUSER**
→ Admin panel only
→ Blocked from front-end
