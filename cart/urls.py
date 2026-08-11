from django.urls import path
from .views import AddToCartView


urlpatterns = [

    path(
        "add/<int:id>/",
        AddToCartView,
        name="add-to-cart"
    ),

]