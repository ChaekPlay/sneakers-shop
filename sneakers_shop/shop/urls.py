from django.urls import path

from .views import index, product, search, cart, about, checkout, order_status, profile, return_order, return_status, \
    sign_up, sign_in, logout_user, LoginUser, thank_you, product_card

urlpatterns = [
    path("", index, name="index"),
    path("search", search, name="search"),
    path("product/<int:product_id>/", product, name="product"),
    path("cart", cart, name="cart"),
    path("about", about, name="about"),
    path("checkout", checkout, name="checkout"),
    path("orders", order_status, name="orders"),
    path("profile", profile, name="profile"),
    path("returns", return_status, name="returns"),
    path("return/create", return_order, name="create_return"),
    path("signup", sign_up, name="sign_up"),
    path("signin", LoginUser.as_view(), name="sign_in"),
    path('logout/', logout_user, name='logout'),
    path('thank_you/', thank_you, name='thank_you'),
    path('product_card/', product_card, name='product_card'),
]