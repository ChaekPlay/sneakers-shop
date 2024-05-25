from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

from shop.models import *


# Create your views here.


def index(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'shop/index.html',context)

def about(request):
    context = {
        'title': 'О сайте',
    }
    return render(request, 'shop/about.html',context)

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
    product_details = Product.objects.get(id=product_id)
    context = {
        'title': 'Товар',
        'product': product_details,
    }
    return render(request, 'shop/product.html',context)


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
