from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView, name='home'),
    path('shop/', ShopView, name='shop'),
    path('about/', AboutView, name='about'),
]