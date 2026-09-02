from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from .models import Order
from django.db import transaction


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
        item.subtotal = item.product.price * item.quantity
        total += item.subtotal

    if request.method == "POST":
        return redirect("payment")

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


@login_required
def SellerOrdersView(request):

    if request.user.user_type != "seller":

        messages.error(
            request,
            "Only sellers can access this page."
        )

        return redirect("home")

    orders = Order.objects.filter(
        product__seller=request.user
    ).order_by("-created_at")

    context = {
        "orders": orders,
    }

    return render(
        request,
        "orders/seller_orders.html",
        context
    )


@login_required
def UpdateOrderStatusView(request, id):

    if request.user.user_type != "seller":

        messages.error(
            request,
            "Only sellers can update orders."
        )

        return redirect("home")


    order = get_object_or_404(
        Order,
        id=id,
        product__seller=request.user
    )


    if request.method == "POST":

        new_status = request.POST.get("status")

        valid_statuses = [
            "pending",
            "confirmed",
            "shipped",
            "delivered",
            "cancelled",
        ]


        if new_status not in valid_statuses:

            messages.error(
                request,
                "Invalid order status."
            )

            return redirect("seller-orders")


        # Reduce stock only when order is approved
        if (
            order.status == "pending"
            and new_status == "confirmed"
        ):

            product = order.product

            if product.stock < order.quantity:

                messages.error(
                    request,
                    "Not enough stock available to confirm this order."
                )

                return redirect("seller-orders")


            with transaction.atomic():

                product.stock -= order.quantity
                product.save()

                order.status = "confirmed"
                order.save()


        else:

            order.status = new_status
            order.save()


        messages.success(
            request,
            "Order status updated successfully."
        )


    return redirect("seller-orders")