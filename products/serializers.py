from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_children(self, obj):
        return ProductSerializer(obj.children.all(), many=True).data

# from rest_framework import serializers

# from .models import DataType, Product, MarketplaceProduct, ProductAttribute, ProductAttributeType
# from marketplaces.models import Marketplace

# class ProductChildrenMinimalSerializer(serializers.ModelSerializer):
#     marketplaces = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = ["id", "parent", "name", "sku", "reference", "image", "marketplaces"]

#     def get_marketplaces(self, obj):
#         return Marketplace.objects.filter(marketplace_products__product=obj).values_list("id", flat=True)    

# class ProductParentMinimalSerializer(serializers.ModelSerializer):
#     marketplaces = serializers.SerializerMethodField()
#     children = ProductChildrenMinimalSerializer(many=True)

#     class Meta:
#         model = Product
#         fields = ["id", "parent", "name", "sku", "reference", "image", "marketplaces", "children"]

#     def get_marketplaces(self, obj):
#         return Marketplace.objects.filter(marketplace_products__product=obj, marketplace_products__enabled=True).values_list("id", flat=True)

# class ProductAttributeTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductAttributeType
#         fields = ["id", "name", "data_type"]

# class ProductAttributeSerializer(serializers.ModelSerializer):
#     attribute_type = ProductAttributeTypeSerializer()
#     data = serializers.SerializerMethodField()
#     data_input = serializers.CharField(write_only=True, required=False)

#     class Meta:
#         model = ProductAttribute
#         fields = ["id", "attribute_type", "data_type", "data", "data_input"]

#     def get_data(self, obj):
#         type_field_map = {
#             DataType.INT: "data_int",
#             DataType.DECIMAL: "data_decimal",
#             DataType.STRING: "data_string",
#             DataType.TEXT: "data_text",
#             DataType.DATE: "data_date",
#             DataType.DATETIME: "data_datetime",
#             DataType.BOOLEAN: "data_boolean",
#         }
#         field_name = type_field_map.get(obj.data_type)
#         return getattr(obj, field_name, None)
    
#     def to_internal_value(self, data):
#         ret = super().to_internal_value(data)
#         value = data.get("data")
#         data_type = ret.get("data_type")

#         field_map = {
#             DataType.INT: "data_int",
#             DataType.DECIMAL: "data_decimal",
#             DataType.STRING: "data_string",
#             DataType.TEXT: "data_text",
#             DataType.DATE: "data_date",
#             DataType.DATETIME: "data_datetime",
#             DataType.BOOLEAN: "data_boolean",
#         }

#         if data_type and value is not None:
#             field = field_map.get(data_type)
#             if field:
#                 ret[field] = value

#         return ret

# class ProductChildrenSerializer(serializers.ModelSerializer):
#     marketplaces = serializers.SerializerMethodField()
#     attributes = ProductAttributeSerializer(many=True)

#     class Meta:
#         model = Product
#         fields = ["id", "parent", "name", "sku", "reference", "price", "stock", "image", "marketplaces", "attributes"]

#     def get_marketplaces(self, obj):
#         return Marketplace.objects.filter(marketplace_products__product=obj).values_list("id", flat=True)    


# class ProductSerializer(serializers.ModelSerializer):
#     marketplaces = serializers.SerializerMethodField()
#     attributes = ProductAttributeSerializer(many=True)
#     children = ProductChildrenSerializer(many=True)

#     class Meta:
#         model = Product
#         fields = ["id", "parent", "name", "sku", "reference", "price", "stock", "image", "marketplaces", "attributes", "children"]

#     def get_marketplaces(self, obj):
#         return Marketplace.objects.filter(marketplace_products__product=obj, marketplace_products__enabled=True).values_list("id", flat=True)
    
#     def update(self, instance, validated_data):
#         attributes_data = validated_data.pop("attributes", None)
#         children_data = validated_data.pop("children", None)

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         if attributes_data is not None:
#             instance.attributes.all().delete()
#             for attr_data in attributes_data:
#                 ProductAttribute.objects.create(product=instance, **attr_data)

#         if children_data is not None:
#             child_ids = [child["id"] for child in children_data]
#             children = Product.objects.filter(id__in=child_ids)
#             instance.children.set(children)

#         return instance

# class MarketplaceProductSerializer(serializers.ModelSerializer):
#     product = ProductSerializer()

#     class Meta:
#         model = MarketplaceProduct
#         fields = "__all__"