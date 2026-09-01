from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from orders.models import Order


def SellerDashboardView(request):

    products = Product.objects.filter(seller=request.user)

    context = {
        "products": products,
    }

    return render(request, "seller/dashboard.html", context)


def AddProductView(request):

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

        return redirect("seller-dashboard")

    return render(request, "seller/add_product.html")


def EditProductView(request, id):

    product = get_object_or_404(
        Product,
        id=id,
        seller=request.user,
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

        return redirect("seller-dashboard")

    context = {
        "product": product,
    }

    return render(request, "seller/edit_product.html", context)

def DeleteProductView(request, id):

    product = get_object_or_404(
        Product,
        id=id,
        seller=request.user
    )

    product.delete()

    return redirect("seller-dashboard")

def ProductDetailView(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    context = {
        "product": product,
    }

    return render(
        request,
        "product_detail.html",
        context
    )

@login_required
def SellerOrdersView(request):

    if request.user.user_type != "seller":
        return redirect("home")

    orders = Order.objects.filter(
        product__seller=request.user
    ).order_by("-created_at")

    context = {
        "orders": orders,
    }

    return render(
        request,
        "seller/orders.html",
        context
    )