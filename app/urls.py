from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home,name="home"),
    path('search/', views.search, name="search"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
]
