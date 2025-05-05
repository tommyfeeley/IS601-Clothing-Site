from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import json
import os

# Create your views here.

def home(request):
    json_path = os.path.join(settings.BASE_DIR, 'base','data', 'products.json')
    with open(json_path, 'r') as file:
        products = json.load(file)
    return render(request, 'home.html', {'products': products})
def cart(request):
    return render(request, 'cart.html')
def thanks(request):
    return render(request, 'thanks.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        json_path = os.path.join(settings.BASE_DIR, 'base', 'data', 'accounts.json')
        with open(json_path, 'r') as file:
            accounts = json.load(file)
        found = False
        for account in accounts:
            if account['username'] == username:
                messages.error(request, 'Username already taken.')
                return render(request, 'register.html')
        new_user = {
            'username': username, 'password': password
                    } 
        accounts.append(new_user)

        with open(json_path, 'w') as file:
            json.dump(accounts, file, indent=5)
        messages.success(request, 'Account created!')
        return redirect('realLoginURL')
    return render(request, 'register.html')

def loginRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        json_path = os.path.join(settings.BASE_DIR, 'base', 'data', 'accounts.json')
        with open(json_path, 'r') as file:
            accounts = json.load(file)
        
        user = None
        for account in accounts:
            if account['username'] == username and account['password'] == password:
                user = account
                break
        

        if user is not None:
            request.session['username'] = username
            return redirect('homeURL')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'loginRegister.html')