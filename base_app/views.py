from django.shortcuts import render

# Create your views here.

def HomeView(request):
    return render(request,'home.html')

def ShopView(request):
    return render(request,'shop.html')

def AboutView(request):
    return render(request,'about.html')

def ProductDetailView(request):
    return render(request, 'product_detail.html')

def RegisterView(request):
    return render(request, 'register.html')
def LoginView(request):
    return render(request,'login.html')

# def HomeView(request):
#     pass
