from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser
from products.models import Product
from orders.models import Order


def HomeView(request):

    featured_products = Product.objects.order_by(
        "-created_at"
    )[:4]

    context = {
        "featured_products": featured_products,
    }

    return render(
        request,
        "home.html",
        context
    )


def ShopView(request):

    category = request.GET.get("category")
    search_query = request.GET.get("q")

    products = Product.objects.all()

    # Search products
    if search_query:
        products = products.filter(
            name__icontains=search_query
        )

    # Category filter
    if category:
        products = products.filter(
            category=category
        )

    categories = Product.CATEGORY_CHOICES

    context = {
        "products": products,
        "categories": categories,
        "selected_category": category,
        "search_query": search_query,
    }

    return render(
        request,
        "shop.html",
        context
    )


def AboutView(request):

    return render(
        request,
        "about.html"
    )


def ProductDetailView(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    context = {
        "product": product
    }

    return render(
        request,
        "product_detail.html",
        context
    )


def RegisterView(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        user_type = request.POST.get("user_type")

        # Password match
        if password1 != password2:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("register")

        # Username already exists
        if CustomUser.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")

        # Email already exists
        if CustomUser.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email already exists."
            )

            return redirect("register")

        # Create user
        CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            password=password1,
            user_type=user_type,
        )

        messages.success(
            request,
            "Account created successfully!"
        )

        return redirect("login")

    return render(
        request,
        "register.html"
    )


def LoginView(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            messages.success(
                request,
                "Login Successful!"
            )

            return redirect("home")

        else:

            messages.error(
                request,
                "Invalid Username or Password."
            )

            return redirect("login")

    return render(
        request,
        "login.html"
    )


def LogoutView(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("home")


@login_required
def SellerDashboardView(request):

    # Only sellers can access the dashboard
    if request.user.user_type != "seller":

        messages.error(
            request,
            "Only sellers can access this page."
        )

        return redirect("home")

    # Get products belonging to this seller
    products = Product.objects.filter(
        seller=request.user
    ).order_by("-created_at")

    # Get orders for this seller's products
    orders = Order.objects.filter(
        product__seller=request.user
    )

    # Total number of orders
    total_orders = orders.count()

    # Calculate revenue
    # Cancelled orders are not included.
    total_revenue = sum(
        order.total_price
        for order in orders
        if order.status != "cancelled"
    )

    context = {
        "products": products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
    }

    return render(
        request,
        "seller/dashboard.html",
        context
    )


@login_required
def ProfileView(request):

    if request.method == "POST":

        request.user.first_name = request.POST.get(
            "first_name"
        )

        request.user.last_name = request.POST.get(
            "last_name"
        )

        request.user.email = request.POST.get(
            "email"
        )

        request.user.phone_number = request.POST.get(
            "phone_number"
        )

        request.user.address = request.POST.get(
            "address"
        )

        if request.FILES.get("profile_image"):

            request.user.profile_image = request.FILES.get(
                "profile_image"
            )

        request.user.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("profile")

    return render(
        request,
        "profile.html"
    )