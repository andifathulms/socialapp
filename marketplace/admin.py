from django.contrib import admin

from .models import Product, ProductImage, ProductCategory, ProductSubCategory, ProductCondition, ProductAvailability

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)
admin.site.register(ProductCondition)
admin.site.register(ProductAvailability)
