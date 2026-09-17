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

    if request.method != "POST":
        return redirect("seller-orders")

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

    current_status = order.status
    product = order.product

    # Pending → Confirmed
    # Reduce stock when seller confirms the order.
    if current_status == "pending" and new_status == "confirmed":

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

        messages.success(
            request,
            "Order confirmed successfully."
        )

        return redirect("seller-orders")

    # Pending → Cancelled
    if current_status == "pending" and new_status == "cancelled":

        order.status = "cancelled"
        order.save()

        messages.success(
            request,
            "Order cancelled successfully."
        )

        return redirect("seller-orders")

    # Confirmed → Shipped
    if current_status == "confirmed" and new_status == "shipped":

        order.status = "shipped"
        order.save()

        messages.success(
            request,
            "Order marked as shipped."
        )

        return redirect("seller-orders")

    # Confirmed → Cancelled
    # Return the previously deducted stock.
    if current_status == "confirmed" and new_status == "cancelled":

        with transaction.atomic():

            product.stock += order.quantity
            product.save()

            order.status = "cancelled"
            order.save()

        messages.success(
            request,
            "Order cancelled and stock restored."
        )

        return redirect("seller-orders")

    # Shipped → Delivered
    if current_status == "shipped" and new_status == "delivered":

        order.status = "delivered"
        order.save()

        messages.success(
            request,
            "Order marked as delivered."
        )

        return redirect("seller-orders")

    # Delivered or already cancelled
    if current_status in ["delivered", "cancelled"]:

        messages.error(
            request,
            "This order can no longer be updated."
        )

        return redirect("seller-orders")

    # Any other invalid transition
    messages.error(
        request,
        "This order status cannot be changed that way."
    )

    return redirect("seller-orders")