from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

from shop.models import *


# Create your views here.


def index(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'shop/index.html', context)


def about(request):
    context = {
        'title': 'О сайте',
    }
    return render(request, 'shop/about.html', context)


def profile(request):
    context = {
        'title': 'Профиль',
    }
    return render(request, 'shop/profile.html', context)


def sign_up(request):
    context = {
        'title': 'Регистрация',
    }
    return render(request, 'shop/sign_up.html', context)

def sign_in(request):
    context = {
        'title': 'Войти',
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


def order_status(request):
    context = {
        'title': 'Статус заказа',
    }
    return render(request, 'shop/order_status.html', context)


def checkout(request):
    context = {
        'title': 'Оформление заказа',
    }
    return render(request, 'shop/checkout.html', context)


def return_order(request):
    context = {
        'title': 'Возврат',
    }
    return render(request, 'shop/return.html', context)


def return_status(request):
    context = {
        'title': 'Статус возврата',
    }
    return render(request, 'shop/return_status.html', context)


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
