from rest_framework import serializers

from .models import Product, MarketplaceProduct
from marketplaces.models import Marketplace

class ProductChildrenMinimalSerializer(serializers.ModelSerializer):
    marketplaces = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "parent", "name", "sku", "reference", "image", "marketplaces"]

    def get_marketplaces(self, obj):
        return Marketplace.objects.filter(marketplace_products__product=obj).values_list("id", flat=True)    

class ProductParentMinimalSerializer(serializers.ModelSerializer):
    marketplaces = serializers.SerializerMethodField()
    children = ProductChildrenMinimalSerializer(many=True)

    class Meta:
        model = Product
        fields = ["id", "parent", "name", "sku", "reference", "image", "marketplaces", "children"]

    def get_marketplaces(self, obj):
        return Marketplace.objects.filter(marketplace_products__product=obj, marketplace_products__enabled=True).values_list("id", flat=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class MarketplaceProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = MarketplaceProduct
        fields = "__all__"