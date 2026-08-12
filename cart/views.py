from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from .models import Cart


def AddToCartView(request, id):

    if not request.user.is_authenticated:
        messages.error(request, "Please login to add products to cart.")
        return redirect("login")

    product = Product.objects.get(id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(
        request,
        f"{product.name} added to your cart."
    )

    return redirect("product-detail", id=product.id)


def CartView(request):

    if not request.user.is_authenticated:
        messages.error(request, "Please login to view your cart.")
        return redirect("login")

    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    context = {
        "cart_items": cart_items,
        "total": total,
    }

    return render(
        request,
        "cart/cart.html",
        context
    )