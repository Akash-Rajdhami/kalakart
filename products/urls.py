from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path(
        "seller/dashboard/",
        SellerDashboardView,
        name="seller-dashboard"
    ),

    path(
        "seller/add-product/",
        AddProductView,
        name="add-product"
    ),

    path(
        "seller/edit-product/<int:id>/",
        EditProductView,
        name="edit-product"
    ),

    path(
        "seller/delete-product/<int:id>/",
        DeleteProductView,
        name="delete-product"
    ),

    path(
        "product/<int:id>/",
        ProductDetailView,
        name="product-detail"
    ),

    path(
    "seller/orders/",
    SellerOrdersView,
    name="seller-orders"
),

]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)