from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404

from shop.forms import CheckoutForm, EditProfileForm, ReturnForm, EditUserForm, LoginUserForm, RegisterUserForm
from shop.models import *


# Create your views here.


def index(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'shop/index.html', context)


def logout_user(request):
    logout(request)
    return redirect('index')


def about(request):
    context = {
        'title': 'О сайте',
    }
    return render(request, 'shop/about.html', context)


@login_required(login_url='sign_in')
def profile(request):
    client = Client.objects.get(id=request.user.id)
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=client.user)
        client_form = EditProfileForm(request.POST, instance=client)
        if user_form.is_valid() and client_form.is_valid():
            user_form.save()
            client_form.save()
            return redirect('profile')
    else:
        user_form = EditUserForm()
        client_form = EditProfileForm()
    context = {
        'title': 'Профиль',
        'client': client,
        'user_form': user_form,
        'client_form': client_form,
    }
    return render(request, 'shop/profile.html', context)


def sign_up(request):
    if request.method == 'POST':
        register_form = RegisterUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            return redirect('index')
    else:
        register_form = RegisterUserForm()
    context = {
        'title': 'Регистрация',
        'form': register_form
    }
    return render(request, 'shop/sign_up.html', context)


def sign_in(request):
    if request.method == 'POST':
        login_form = LoginUserForm(request.POST)
        user = authenticate(request, email=login_form.email, password=login_form.password)
        if user is not None:
            login(request, user)
            return redirect('index')
    else:
        login_form = LoginUserForm()
    context = {
        'title': 'Войти',
        'form': login_form
    }
    return render(request, 'shop/sign_in.html', context)


def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query)
    context = {
        'title': 'Результаты поиска',
        'query': query,
        'products': products,
    }
    return render(request, 'shop/search.html', context)


def product(request, product_id):
    try:
        product_details = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404()
    context = {
        'title': 'Товар',
        'product': product_details,
    }
    return render(request, 'shop/product.html', context)


@login_required(login_url='sign_in')
def order_status(request, orderid):
    order = Order.objects.get(id=orderid)
    if request.user.id != order.client.id:
        return redirect('index')
    context = {
        'title': 'Статус заказа',
        'order': order
    }
    return render(request, 'shop/order_status.html', context)


@login_required(login_url='sign_in')
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_status')
    else:
        form = CheckoutForm()
    context = {
        'title': 'Оформление заказа',
        'form': form
    }
    return render(request, 'shop/checkout.html', context)


@login_required(login_url='sign_in')
def return_order(request):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('return_status')
    else:
        form = ReturnForm()
    context = {
        'title': 'Возврат',
        'form': form,
    }
    return render(request, 'shop/return.html', context)


@login_required(login_url='sign_in')
def return_status(request):
    context = {
        'title': 'Статус возврата',
    }
    return render(request, 'shop/return_status.html', context)


@login_required(login_url='sign_in')
def cart(request):
    context = {
        'title': 'Корзина',
    }
    return render(request, 'shop/cart.html', context)


def page_not_found(request, exception):
    context = {
        'title': 'Страница не найдена',
    }
    return render(request, 'general/not_found.html', status=404)
