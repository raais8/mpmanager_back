from rest_framework import serializers

from .models import Order, Customer, Carrier, OrderItem

from marketplaces.serializers import MarketplaceSerializer
from products.serializers import MarketplaceProductSerializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class CustomerMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "bill_firstname", "bill_lastname", "bill_country"]

class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    marketplace_product = MarketplaceProductSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    carrier = CarrierSerializer()
    marketplace = MarketplaceSerializer()
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"

class OrderMinimalSerializer(serializers.ModelSerializer):
    customer = CustomerMinimalSerializer()
    marketplace = MarketplaceSerializer()

    class Meta:
        model = Order
        fields = ["id", "marketplace", "customer", "order_id", "status", "order_date", "total_price", "ticket"]