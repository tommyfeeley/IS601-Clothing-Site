from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')
def login(request):
    return render(request, 'login.html')
def cart(request):
    return render(request, 'cart.html')
def thanks(request):
    return render(request, 'thanks.html')
