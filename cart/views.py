from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Cart


def AddToCartView(request, id):

    if not request.user.is_authenticated:
        messages.error(request, "Please login to add products to cart.")
        return redirect("login")

    product = get_object_or_404(Product, id=id)

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