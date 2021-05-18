from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def registerPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)

                return redirect('login')

        context = {
            'form': form
        }
        return render(request, 'register.html/', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'login.html/', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):

    URL = 'https://api.binance.com/api/v3/avgPrice?symbol={}'

    coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'BCHUSDT', 'LTCUSDT']
    data = []
    for coin in coins:
        res = requests.get(URL.format(coin))
        coin_info = {
            'name': coin,
            'price': round(float(res.json()['price']), 2),
        }
        data.append(coin_info)

    context = {
        'data': data
    }
    return render(request, 'home.html/', context)