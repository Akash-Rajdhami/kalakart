from django.urls import path

from .views import (
    CheckoutView,
    OrderSuccessView,
    MyOrdersView,
    SellerOrdersView,
    UpdateOrderStatusView,
)


urlpatterns = [

    path(
        "checkout/",
        CheckoutView,
        name="checkout"
    ),

    path(
        "order-success/",
        OrderSuccessView,
        name="order-success"
    ),

    path(
        "my-orders/",
        MyOrdersView,
        name="my-orders"
    ),

    path(
        "seller-orders/",
        SellerOrdersView,
        name="seller-orders"
    ),

    path(
        "update-status/<int:id>/",
        UpdateOrderStatusView,
        name="update-order-status"
    ),

]