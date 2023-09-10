from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('base/', views.base, name='base'),
    path('', views.index, name='index'),
    path('register/', views.register),
    path('login/', views.login , name='login'),
    path('logout/', auth_views.LoginView.as_view(template_name='logout.html')),
    path('verify/', views.verify_code, name='verify'),
    path('product/<str:pk>/', views.product, name='product-details'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    path('profile/', views.profile, name='profile'),
    path('purchase/', views.purchase, name='purchase'),
]