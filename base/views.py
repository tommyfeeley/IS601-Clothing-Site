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

    sort = request.GET.get('sort')

    if sort == 'ascending':
        for x in range(len(products)):
            for y in range(len(products) - 1):
                if products[y]['price'] > products[y+1]['price']:
                    temp_var = products[y]
                    products[y] = products[y + 1] 
                    products[y+1] = temp_var

    elif sort == 'descending':
        for x in range(len(products)):
            for y in range(len(products) - 1):
                if products[y]['price'] < products[y+1]['price']:
                    temp_var = products[y]
                    products[y] = products[y + 1] 
                    products[y+1] = temp_var

    return render(request, 'home.html', {'products': products, 'sort': sort})

def nav(request):
    cart_size = 0
    cart = request.session.get('cart', {})
    for item in cart.items():
        cart_size += 1
    return render(request, 'nav.html', {'cart_size': cart_size})

def cart(request):
    cart = request.session.get('cart', {})
    json_path = os.path.join(settings.BASE_DIR, 'base', 'data', 'products.json')
    with open(json_path, 'r') as file:
        products = json.load(file)
    cart_items = []
    total = 0

    for cart_key, item in cart.items():
        product_id = item['product_id']
        product = None
        for x in products:
            if str(x['id']) == product_id:
                product = x
                break
        if product is not None:
            subtotal = float(product['price']) * float(item['quantity'])
            cart_items.append({
                'id': product_id, 'name': product['name'], 'image': product['image'], 'size': item['size'], 'quantity': item['quantity'], 'price': product['price'], 'subtotal': subtotal
            })
        total += subtotal
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

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
        new_user = { 'username': username, 'password': password } 
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
def logout(request):
    request.session.flush()
    return redirect('homeURL')

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        size = request.POST.get('size')
        quantity = request.POST.get('quantity', 1)

        cart = request.session.get('cart', {})
        cart_key = f"{product_id}_{size}"

        if cart_key in cart:
            cart[cart_key]['quantity'] += quantity
        else:
            cart[cart_key] = {
                'product_id': product_id,
                'size': size,
                'quantity': quantity
            }
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('homeURL')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    for key in list(cart.keys()):
        if cart[key]['product_id'] == product_id:
            del cart[key]
            break
    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cartURL')

def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        cart = request.session.get('cart', {})

        for key in cart:
            if cart[key]['product_id'] == product_id:
                if quantity > 0:
                    cart[key]['quantity'] = quantity
                else:
                    del cart[key]
                break
        request.session['cart'] = cart
        request.session.modified = True

        return redirect('cartURL')
    
def thanks(request):
    ordered_items = []
    total = 0

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        json_path = os.path.join(settings.BASE_DIR, 'base', 'data', 'products.json')
        with open(json_path, 'r') as file:
            products = json.load(file)

        for cart_key, item in cart.items():
            product_id = item['product_id']
            product = None
            for x in products:
                if str(x['id']) == product_id:
                    product = x
                    break
            if product is not None:
                subtotal = float(product['price']) * float(item['quantity'])
                ordered_items.append({'id': product_id, 'name': product['name'], 'image': product['image'], 'size': item['size'], 'quantity': item['quantity'], 'price': product['price'], 'subtotal': subtotal })
                total += subtotal
        request.session['cart'] = {}
        request.session.modified = True

    return render(request, 'thanks.html', {'ordered_items':ordered_items, 'total': total})