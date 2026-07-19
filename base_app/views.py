from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login, logout

def HomeView(request):
    return render(request, "home.html")


def ShopView(request):
    return render(request, "shop.html")


def AboutView(request):
    return render(request, "about.html")


def ProductDetailView(request):
    return render(request, "product_detail.html")


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
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # Create user
        CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            password=password1,
            user_type=user_type,
        )

        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "register.html")


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

            login(request, user)

            messages.success(request, "Login Successful!")

            return redirect("home")

        else:

            messages.error(request, "Invalid Username or Password.")

            return redirect("login")

    return render(request, "login.html")

def LogoutView(request):

    logout(request)

    messages.success(request, "Logged out successfully.")

    return redirect("home")