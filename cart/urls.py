from django.urls import path

from .views import (
    AddToCartView,
    CartView,
    IncreaseQuantityView,
    DecreaseQuantityView,
    RemoveFromCartView,
)


urlpatterns = [

    path(
        "add/<int:id>/",
        AddToCartView,
        name="add-to-cart"
    ),

    path(
        "",
        CartView,
        name="cart"
    ),

    path(
        "increase/<int:id>/",
        IncreaseQuantityView,
        name="increase-quantity"
    ),

    path(
        "decrease/<int:id>/",
        DecreaseQuantityView,
        name="decrease-quantity"
    ),

    path(
        "remove/<int:id>/",
        RemoveFromCartView,
        name="remove-from-cart"
    ),

]