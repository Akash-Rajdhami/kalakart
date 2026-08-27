from django.urls import path

from .views import (
    CheckoutView,
    OrderSuccessView,
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

]