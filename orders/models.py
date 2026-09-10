from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

from cart.models import Cart
from .models import Order


@login_required
def CheckoutView(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    if not cart_items.exists():
        messages.error(
            request,
            "Your cart is empty."
        )
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

        old_status = order.status
        product = order.product

        # Pending → Confirmed
        # Reduce product stock.
        if (
            old_status == "pending"
            and new_status == "confirmed"
        ):

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

        # Confirmed → Cancelled
        # Restore the previously deducted stock.
        elif (
            old_status == "confirmed"
            and new_status == "cancelled"
        ):

            with transaction.atomic():

                product.stock += order.quantity
                product.save()

                order.status = "cancelled"
                order.save()

        # Delivered and cancelled orders
        # cannot be changed again.
        elif old_status in [
            "delivered",
            "cancelled"
        ]:

            messages.error(
                request,
                "This order can no longer be updated."
            )

            return redirect("seller-orders")

        # Other valid status changes.
        else:

            order.status = new_status
            order.save()

        messages.success(
            request,
            "Order status updated successfully."
        )

    return redirect("seller-orders")