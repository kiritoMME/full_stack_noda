from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('base/', views.base, name='base'),
    path('', views.index, name='index'),
    path('registerPage/', views.registerPage, name='registerPage'),
    path('login/', views.login , name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify/', views.verify_code, name='verify'),
    path('product/<str:pk>/', views.product, name='product-details'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    path('addToCart/<str:productid>/<str:count>', views.addToCart, name='addToCart'),
    path('profile/', views.profile, name='profile'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('changeProfile/', views.changeProfile, name='changeProfile'),
    path('purchase/', views.purchase, name='purchase'),
    path('pay/', views.pay, name='pay'),
    path('myOrders/', views.myOrders, name='myOrders'),


    # admins
    path('adminOrders/', views.adminOrders, name='adminOrders'),
    path('adminConfOrderDetails/<str:id>/', views.adminConfOrderDetails, name='adminConfOrderDetails'),
]