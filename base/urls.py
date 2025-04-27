from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="homeURL"),
    path('login/', views.login, name="loginURL"),
    path('cart/', views.cart, name="cartURL"),
    path('thanks/', views.thanks, name="thanksURL")
]