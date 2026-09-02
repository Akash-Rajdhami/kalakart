from django.urls import path
from .views import (
SellerDashboardView,
AddProductView,
EditProductView,
DeleteProductView,
)

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


]

urlpatterns += static(
settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT
)
