from django.urls import path
from .views import (
    digital_product_list,
    digital_product_detail,
    download_digital_product,
)

urlpatterns = [
    path("", digital_product_list),
    path("<slug:slug>/", digital_product_detail),
    path("download/<int:product_id>/", download_digital_product),
]
