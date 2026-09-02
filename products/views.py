
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product


@login_required
def SellerDashboardView(request):

    if request.user.user_type != "seller":
        messages.error(request, "Only sellers can access this page.")
        return redirect("home")

    products = Product.objects.filter(
        seller=request.user
    )

    context = {
        "products": products
    }

    return render(
        request,
        "seller/dashboard.html",
        context
    )


@login_required
def AddProductView(request):

    if request.user.user_type != "seller":
        messages.error(request, "Only sellers can add products.")
        return redirect("home")

    if request.method == "POST":

        Product.objects.create(
            seller=request.user,
            name=request.POST.get("name"),
            category=request.POST.get("category"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
            image=request.FILES.get("image"),
        )

        messages.success(
            request,
            "Product added successfully."
        )

        return redirect("seller-dashboard")

    return render(
        request,
        "seller/add_product.html"
    )


@login_required
def EditProductView(request, id):

    if request.user.user_type != "seller":
        messages.error(request, "Only sellers can edit products.")
        return redirect("home")

    product = get_object_or_404(
        Product,
        id=id,
        seller=request.user
    )

    if request.method == "POST":

        product.name = request.POST.get("name")
        product.category = request.POST.get("category")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()

        messages.success(
            request,
            "Product updated successfully."
        )

        return redirect("seller-dashboard")

    context = {
        "product": product
    }

    return render(
        request,
        "seller/edit_product.html",
        context
    )


@login_required
def DeleteProductView(request, id):

    if request.user.user_type != "seller":
        messages.error(request, "Only sellers can delete products.")
        return redirect("home")

    product = get_object_or_404(
        Product,
        id=id,
        seller=request.user
    )

    product.delete()

    messages.success(
        request,
        "Product deleted successfully."
    )

    return redirect("seller-dashboard")

