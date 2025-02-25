from rest_framework import serializers

from .models import Order, Customer, Carrier

from marketplaces.serializers import MarketplaceSerializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    carrier = CarrierSerializer()
    marketplace = MarketplaceSerializer()

    class Meta:
        model = Order
        fields = "__all__"