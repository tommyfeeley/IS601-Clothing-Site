from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="homeURL"),
    path('cart/', views.cart, name="cartURL"),
    path('thanks/', views.thanks, name="thanksURL"),
    path('loginRegister/', views.loginRegister, name="realLoginURL"),
    path('register/',views.register, name="registerURL"),
    path('logout/', views.logout, name='logout'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
]