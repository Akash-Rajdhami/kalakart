from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def PaymentView(request):

    return render(
        request,
        "payments/payment.html"
    )


@login_required
def PaymentSuccessView(request):

    return render(
        request,
        "payments/payment_success.html"
    )


@login_required
def PaymentFailedView(request):

    return render(
        request,
        "payments/payment_failed.html"
    )