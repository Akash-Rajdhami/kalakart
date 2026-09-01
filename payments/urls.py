from django.urls import path

from .views import (
    PaymentView,
    PaymentSuccessView,
    PaymentFailedView,
)


urlpatterns = [

    path(
        "",
        PaymentView,
        name="payment"
    ),

    path(
        "success/",
        PaymentSuccessView,
        name="payment-success"
    ),

    path(
        "failed/",
        PaymentFailedView,
        name="payment-failed"
    ),

]