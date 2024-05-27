from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse_lazy

from shop.forms import CheckoutForm, EditProfileForm, ReturnForm, EditUserForm, LoginUserForm, RegisterUserForm, \
    CreateClientForm
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
    user = User.objects.get(id=request.user.id)
    client = Client.objects.get(user_id=user.id)
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
        client_form = CreateClientForm(request.POST)
        if register_form.is_valid() and client_form.is_valid():
            user = register_form.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            login(request, user)
            return redirect('index')
    else:
        register_form = RegisterUserForm()
        client_form = CreateClientForm()
    context = {
        'title': 'Регистрация',
        'user_form': register_form,
        'client_form': client_form
    }
    return render(request, 'shop/sign_up.html', context)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'shop/sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'title': 'Войти'}
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('index')

def sign_in(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
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
    if query is None:
        products = Product.objects.all()
    else:
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


def thank_you(request):
    context = {
        'title': 'Спасибо!',
    }
    return render(request, 'shop/thank_you.html', context)

def product_card(request):
    context = {
        'title': 'Товар',
    }
    return render(request, 'shop/product_card.html', context)


@login_required(login_url='sign_in')
def order_status(request):
    user = User.objects.get(id=request.user.id)
    client = Client.objects.get(user_id=user.id)
    orders = Order.objects.filter(client_id=client.id)
    context = {
        'title': 'Статус заказа',
        'orders': orders
    }
    return render(request, 'shop/order_status.html', context)


#"@login_required(login_url='sign_in')
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


#@login_required(login_url='sign_in')
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
