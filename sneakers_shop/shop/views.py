from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.


def index(request):
    return render(request, 'shop/index.html')


def search(request):
    return HttpResponse(
        f"<h1>Hello, world!</h1> <p>query: {request.GET.get('q')}</p>"
    )  # render(request, 'shop/search.html')


def product(request, productid):
    return HttpResponse(
        f"<h1>Hello, world!</h1> product: {productid}"
    )  # render(request, 'shop/product.html')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")
