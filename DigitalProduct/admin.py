# digitalproduct/admin.py
from django.contrib import admin
from .models import (
    DigitalProductCategory,
    DigitalProduct,
    DigitalProductBundle,
    DigitalProductPurchase,
    DigitalProductBundlePurchase,
)

admin.site.register(DigitalProductCategory)
admin.site.register(DigitalProduct)
admin.site.register(DigitalProductBundle)
admin.site.register(DigitalProductPurchase)
admin.site.register(DigitalProductBundlePurchase)
