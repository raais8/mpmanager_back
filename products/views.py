from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from django.db.models import Q

from .models import Product, ProductAttribute, ProductAttributeType

from .serializers import ProductParentMinimalSerializer, ProductSerializer, ProductAttributeSerializer, ProductAttributeTypeSerializer
from .pagination import ProductPagination

from itertools import chain

class ProductListView(ListAPIView):
    queryset = Product.objects.filter(parent__isnull=True).order_by("id")
    serializer_class = ProductParentMinimalSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        marketplaces = self.request.query_params.get("marketplace")
        search = self.request.query_params.get("search")

        if not marketplaces:
            return queryset.none()

        if search:
            matching_products = Product.objects.filter(
                Q(name__icontains=search) |
                Q(sku__icontains=search) |
                Q(reference__icontains=search)
            )
            parent_ids = matching_products.values_list("parent", flat=True)
            queryset = queryset.filter(
                Q(id__in=matching_products.values_list("id", flat=True)) |
                Q(id__in=parent_ids)
            )

        marketplaces_list = marketplaces.split(",")

        if "0" in marketplaces_list:
            filter_conditions = Q(marketplaceproduct__marketplace_id__in=marketplaces_list) | (Q(marketplaceproduct__isnull=True) & Q(children__isnull=True))
        else:
            filter_conditions = Q(marketplaceproduct__marketplace_id__in=marketplaces_list)

        matching_products_with_marketplace = Product.objects.filter(filter_conditions).values_list("id", "parent")

        product_ids = set(chain(*matching_products_with_marketplace))

        queryset = queryset.filter(id__in=product_ids)

        return queryset

class ProductView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductAttributeListView(ListAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer

class ProductAttributeTypeListView(ListAPIView):
    queryset = ProductAttributeType.objects.all()
    serializer_class = ProductAttributeTypeSerializer
