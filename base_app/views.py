from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from products.models import Product


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
    selected_sort = request.GET.get("sort")

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


    # Sorting

    if selected_sort == "newest":

        products = products.order_by(
            "-created_at"
        )

    elif selected_sort == "price_low":

        products = products.order_by(
            "price"
        )

    elif selected_sort == "price_high":

        products = products.order_by(
            "-price"
        )

    else:

        products = products.order_by(
            "-created_at"
        )


    categories = Product.CATEGORY_CHOICES


    context = {
        "products": products,
        "categories": categories,
        "selected_category": category,
        "search_query": search_query,
        "selected_sort": selected_sort,
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

        # Get name from the form
        full_name = (
            request.POST.get("full_name")
            or request.POST.get("name")
            or request.POST.get("first_name")
            or ""
        ).strip()

        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        user_type = request.POST.get("user_type")

        # Validate name
        if not full_name:
            messages.error(request, "Please enter your full name.")
            return redirect("register")

        # Separate first name and last name
        name_parts = full_name.split()

        first_name = name_parts[0]

        if len(name_parts) > 1:
            last_name = " ".join(name_parts[1:])
        else:
            last_name = ""

        # Validate username
        if not username:
            messages.error(request, "Please enter a username.")
            return redirect("register")

        # Validate email
        if not email:
            messages.error(request, "Please enter your email.")
            return redirect("register")

        # Validate user type
        if user_type not in ["customer", "seller"]:
            messages.error(request, "Please select Customer or Seller.")
            return redirect("register")

        # Validate passwords
        if not password1 or not password2:
            messages.error(request, "Please enter both passwords.")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check username
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Check email
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # Create user
        CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
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

    if request.user.user_type != "seller":

        messages.error(
            request,
            "Only sellers can access this page."
        )

        return redirect("home")


    return render(
        request,
        "seller/dashboard.html"
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