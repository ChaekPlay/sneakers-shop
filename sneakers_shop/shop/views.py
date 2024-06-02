from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView

from shop.forms import CheckoutForm, EditProfileForm, ReturnForm, EditUserForm, LoginUserForm, RegisterUserForm, \
    CreateClientForm
from shop.models import *


# Create your views here.


def index(request):
    products = Product.objects.all()[:5]
    context = {
        'title': 'Главная страница',
        'products': products,
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
            user_cart = Cart.objects.create(client=client)
            user_cart.save()
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


class Search(ListView):
    paginate_by = 9
    model = Product
    template_name = 'shop/search.html'
    context_object_name = 'products'
    context = {
        'title': 'Результаты поиска',
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query is None:
            query = ''
        c_def = {'title': 'Результаты поиска', 'query': query}
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        if self.request.GET.get('q') is not None:
            return Product.objects.filter(name__icontains=self.request.GET.get('q'))
        return Product.objects.all()


def product(request, product_id):
    try:
        product_details = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404()
    context = {
        'title': 'Товар ' + product_details.name,
        'product': product_details,
    }
    return render(request, 'shop/product_card.html', context)


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
    order_set = {}
    for order in orders:
        manager = Manager.objects.get(id=order.manager_id)
        manager_str = manager.user.first_name + ' ' + manager.user.last_name + ', Телефон: ' + manager.phone
        order_set[order.id] = {
            'items': get_order_items(order),
            'manager': manager_str,
            'date': order.delivery_date,
            'status': get_delivery_status(order.delivery_status)
        }
    context = {
        'title': 'Статус заказа',
        'orders': order_set,
    }
    return render(request, 'shop/order_status.html', context)
@login_required(login_url='sign_in')
def accept_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delivery_status = DELIVERY_STATUS[2][0]
    order.save()
    return redirect('orders')

@login_required(login_url='sign_in')
def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delivery_status = DELIVERY_STATUS[3][0]
    order.save()
    return redirect('orders')

def get_delivery_status(status):
    if status == 'PACK':
        return 'Собирается'
    elif status == 'OTW':
        return 'В пути'
    elif status == 'DELD':
        return 'Доставлен'
    elif status == 'CANC':
        return 'Отменен'
def get_order_items(order):
    result_order = {}

    for product in order.products.select_related():
        product_in_return = Return.objects.filter(order_id=order.id, product_id=product.id)
        amount = ProductInOrder.objects.filter(order_id=order.id, product_id=product.id).first().product_count
        result_order[product.id] = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'amount': amount,
            'total_price': product.price * amount,
            'image': product.image,
            'size': product.size,
            'return_made': product_in_return.exists()
        }
    return result_order


def get_random_manager():
    return Manager.objects.all().order_by('?').first()


@login_required(login_url='sign_in')
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            manager_id = get_random_manager().id
            order = Order.objects.create(client_id=Client.objects.get(user_id=request.user.id).id,
                                         delivery_date=form.cleaned_data['delivery_date'], delivery_status='PACK',
                                         delivery_address=form.cleaned_data['delivery_address'], manager_id=manager_id)
            cart = Cart.objects.get(client_id=Client.objects.get(user_id=request.user.id).id)
            for product_in_cart in cart.product_in_cart_fields.all():
                ProductInOrder.objects.create(order_id=order.id, product_id=product_in_cart.product_id,
                                              product_count=product_in_cart.product_count)
            cart.products.clear()
            return redirect('thank_you')
    else:
        form = CheckoutForm()
    result_cart = get_cart(request)
    total_price = get_total_price(result_cart)
    context = {
        'title': 'Оформление заказа',
        'form': form,
        'cart': result_cart,
        'total_price': total_price
    }
    return render(request, 'shop/checkout.html', context)


@login_required(login_url='sign_in')
def return_order(request, order_id, product_id):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            return_obj = Return.objects.create(client_id=Client.objects.get(user_id=request.user.id).id, order_id=order_id, product_id=product_id, reason=form.cleaned_data['reason'], manager_id=get_random_manager().id)
            return_obj.save()
            return redirect('returns')
    else:
        form = ReturnForm()
    context = {
        'title': 'Возврат',
        'form': form,
        'product_id': product_id,
        'order_id': order_id
    }
    return render(request, 'shop/return.html', context)


@login_required(login_url='sign_in')
def return_status(request):
    returns = Return.objects.filter(client_id=Client.objects.get(user_id=request.user.id).id)
    context = {
        'title': 'Статус возврата',
        'returns': get_returning_items(returns),
    }
    return render(request, 'shop/return_status.html', context)

def get_returning_items(returning):
    result_returning = {}
    for return_obj in returning:
        result_returning[return_obj.id] = {
            'id': return_obj.product.id,
            'name': return_obj.product.name,
            'price': return_obj.product.price,
            'image': return_obj.product.image,
            'size': return_obj.product.size,
            'reason': return_obj.reason,
            'date': return_obj.date,
            'manager': return_obj.manager,
            'status': get_return_status(return_obj)
        }
    return result_returning

def get_return_status(returning):
    if returning.status == 'PENDING':
        return 'В обработке'
    elif returning.status == 'ACCEPT':
        return 'Принят'
    elif returning.status == 'DECLINE':
        return 'Отменен'
    else:
        return 'Ошибка'

@login_required(login_url='sign_in')
def accept_return(request, return_id):
    return_obj = Return.objects.get(id=return_id)
    return_obj.status = RETURN_STATUS[1][0]
    return_obj.save()
    return redirect('returns')

@login_required(login_url='sign_in')
def cancel_return(request, return_id):
    return_obj = Return.objects.get(id=return_id)
    return_obj.status = RETURN_STATUS[2][0]
    return_obj.save()
    return redirect('returns')

@login_required(login_url='sign_in')
def cart(request):
    result_cart = get_cart(request)
    total_price = get_total_price(result_cart)
    context = {
        'title': 'Корзина',
        'cart': result_cart,
        'total_price': total_price,
        'is_empty': len(result_cart) == 0
    }
    return render(request, 'shop/cart.html', context)


def get_cart(request):
    cart = Cart.objects.get(client_id=Client.objects.get(user_id=request.user.id).id)
    result_cart = {}
    for product in cart.products.select_related():
        amount = ProductInCart.objects.filter(cart_id=cart.id, product_id=product.id).first().product_count
        result_cart[product.id] = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'amount': amount,
            'total_price': product.price * amount,
            'image': product.image,
            'size': product.size
        }
    return result_cart


def get_total_price(cart):
    total_price = 0
    for product in cart:
        total_price += cart[product]['price'] * cart[product]['amount']
    return total_price


@login_required(login_url='sign_in')
def add_to_cart(request, product_id):
    product_to_add = get_object_or_404(Product, id=product_id)
    client = Client.objects.get(user_id=request.user.id)
    cart = Cart.objects.get(client_id=client.id)
    if not ProductInCart.objects.filter(cart_id=cart.id, product_id=product_id).exists():
        cart.products.add(product_to_add, through_defaults={'product_count': 1})
    else:
        product_count = get_object_or_404(ProductInCart, cart_id=cart.id, product_id=product_id).product_count
        ProductInCart.objects.filter(cart_id=cart.id, product_id=product_id).update(product_count=product_count + 1)
    return redirect('cart')


@login_required(login_url='sign_in')
def remove_from_cart(request, product_id):
    product_to_delete = get_object_or_404(Product, id=product_id)
    client = Client.objects.get(user_id=request.user.id)
    cart = Cart.objects.get(client_id=client.id)
    product_count = ProductInCart.objects.filter(cart_id=cart.id, product_id=product_id).first().product_count
    if product_count == 1:
        cart.products.remove(product_to_delete)
    else:
        ProductInCart.objects.filter(cart_id=cart.id, product_id=product_id).update(product_count=product_count - 1)
    return redirect('cart')


def page_not_found(request, exception):
    context = {
        'title': 'Страница не найдена',
    }
    return render(request, 'general/not_found.html', status=404)
