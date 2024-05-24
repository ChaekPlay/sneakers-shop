from django.urls import path

from .views import index, product, search 

urlpatterns = [
    path("", index, name="index"),
    path("search", search, name="search"),
    path("product/<int:productid>/", product, name="product"),
    # path("cart", cart, name="cart"),
    # path("checkout/<int:orderid>", checkout, name="checkout"),
    # path("order/<int:orderid>", order, name="order"),
    # path("profile", profile, name="profile"),
    # path("return/<int:returnid>", return_order, name="return"),
    # path("return/create", create_return, name="create_return"),
]