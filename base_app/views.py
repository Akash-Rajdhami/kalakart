from django.shortcuts import render

# Create your views here.

def HomeView(request):
    return render(request,'home.html')

def ShopView(request):
    pass

def AboutView(request):
    pass

# def HomeView(request):
#     pass
