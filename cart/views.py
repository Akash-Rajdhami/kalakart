from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from products.models import Product
from .models import Cart


@login_required
def AddToCartView(request, id):

    product = get_object_or_404(Product, id=id)

    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect("product-detail", id=product.id)

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
            return redirect("product-detail", id=product.id)

    messages.success(
        request,
        f"{product.name} added to your cart."
    )

    return redirect("product-detail", id=product.id)


@login_required
def CartView(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = 0

    for item in cart_items:

        item.subtotal = item.product.price * item.quantity

        total += item.subtotal

    context = {
        "cart_items": cart_items,
        "total": total,
    }

    return render(
        request,
        "cart/cart.html",
        context
    )


@login_required
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


@login_required
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


@login_required
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