from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Cart


def AddToCartView(request, id):

    if not request.user.is_authenticated:
        messages.error(
            request,
            "Please login to add products to cart."
        )
        return redirect("login")

    product = get_object_or_404(
        Product,
        id=id
    )

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:

        if cart_item.quantity < product.stock:

            cart_item.quantity += 1
            cart_item.save()

        else:

            messages.error(
                request,
                "You cannot add more than the available stock."
            )

            return redirect(
                "product-detail",
                id=product.id
            )

    messages.success(
        request,
        f"{product.name} added to your cart."
    )

    return redirect(
        "product-detail",
        id=product.id
    )


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


def IncreaseQuantityView(request, id):

    cart_item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    if cart_item.quantity < cart_item.product.stock:

        cart_item.quantity += 1
        cart_item.save()

    else:

        messages.error(
            request,
            "You cannot add more than the available stock."
        )

    return redirect("cart")


def DecreaseQuantityView(request, id):

    cart_item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart")


def RemoveFromCartView(request, id):

    cart_item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    cart_item.delete()

    messages.success(
        request,
        "Product removed from cart."
    )

    return redirect("cart")