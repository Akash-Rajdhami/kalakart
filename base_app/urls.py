from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView, name='home'),
    path('shop/', ShopView, name='shop'),
    path('about/', AboutView, name='about'),
    path('product/', ProductDetailView, name='product-detail'),
    path('register/', RegisterView, name='register'),
    path('login/', LoginView, name='login'),
    path("logout/", LogoutView, name="logout"),
]