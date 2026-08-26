from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from .models import Order


@login_required
def CheckoutView(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":

        for item in cart_items:

            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                total_price=item.product.price * item.quantity,
            )

        cart_items.delete()

        messages.success(
            request,
            "Your order has been placed successfully!"
        )

        return redirect("order-success")

    context = {
        "cart_items": cart_items,
        "total": total,
    }

    return render(
        request,
        "orders/checkout.html",
        context
    )


@login_required
def OrderSuccessView(request):

    return render(
        request,
        "orders/order_success.html"
    )


@login_required
def MyOrdersView(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    context = {
        "orders": orders,
    }

    return render(
        request,
        "orders/my_orders.html",
        context
    )