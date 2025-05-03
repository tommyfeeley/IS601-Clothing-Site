from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, 'home.html')
def cart(request):
    return render(request, 'cart.html')
def thanks(request):
    return render(request, 'thanks.html')

def loginRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homeURL')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'loginRegister.html')