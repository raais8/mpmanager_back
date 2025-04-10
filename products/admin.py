from django.contrib import admin

from .models import Product, MarketplaceProduct, ProductAttribute, ProductAttributeType

admin.site.register(Product)
admin.site.register(MarketplaceProduct)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeType)