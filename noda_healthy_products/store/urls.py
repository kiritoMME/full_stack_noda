from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('base/', views.base, name='base'),
    path('', views.index, name='index'),
    path('register/', views.register),
    path('login/', views.login , name='login'),
    path('logout/', auth_views.LoginView.as_view(template_name='logout.html')),
    path('verify/', views.verify_code),
]