from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="homeURL"),
    path('cart/', views.cart, name="cartURL"),
    path('thanks/', views.thanks, name="thanksURL"),
    path('loginRegister/', views.loginRegister, name="realLoginURL"),
    path('register/',views.register, name="registerURL"),
    path('logout/', views.logout, name='logout')
]