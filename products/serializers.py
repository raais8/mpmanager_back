from rest_framework import serializers

from .models import Product, MarketplaceProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class MarketplaceProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = MarketplaceProduct
        fields = "__all__"