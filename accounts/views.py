from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser


def RegisterView(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        user_type = request.POST.get("user_type")

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Check email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # Create new user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            password=password1,
            user_type=user_type,
        )

        user.save()

        messages.success(request, "Account created successfully!")

        return redirect("login")

    return render(request, "register.html")