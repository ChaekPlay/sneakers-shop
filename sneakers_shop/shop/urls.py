from django.urls import path

from .views import index, product, search, cart, about, checkout, order_status, profile, return_order, return_status, \
    sign_up, sign_in, logout_user

urlpatterns = [
    path("", index, name="index"),
    path("search", search, name="search"),
    path("product/<int:product_id>/", product, name="product"),
    path("cart", cart, name="cart"),
    path("about", about, name="about"),
    path("checkout", checkout, name="checkout"),
    path("order/<int:orderid>", order_status, name="order_status"),
    path("profile", profile, name="profile"),
    path("return/<int:returnid>", return_status, name="return"),
    path("return/create", return_order, name="create_return"),
    path("signup", sign_up, name="sign_up"),
    path("signin", sign_in, name="sign_in"),
    path('logout/', logout_user, name='logout'),
]