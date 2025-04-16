from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from  django.db.models import Q

from .models import Product
from .serializers import ProductSerializer
from .pagination import ProductPagination

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def list(self, request):
        queryset = self.get_queryset().order_by("id")
        paginated = request.query_params.get("paginated", "true").lower() == "true"
        product_ids = request.query_params.get("product_ids")
        marketplace_ids = request.query_params.get("marketplace_ids")
        search = request.query_params.get("search")

        if product_ids:
            try:
                ids = [int(product_id) for product_id in product_ids.split(",")]
                queryset = queryset.filter(id__in=ids)
            except ValueError:
                return Response({"error": "Invalid product_ids parameter"}, status=400)

        else:
            queryset = queryset.filter(parent__isnull=True)
            if not marketplace_ids:
                queryset = queryset.none()
            else:
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

                try:
                    marketplaces_list = [int(marketplace_id) for marketplace_id in marketplace_ids.split(",")]
                except ValueError:
                    return Response({"error": "Invalid marketplace_ids parameter"}, status=400)
                
                if 0 not in marketplaces_list:
                    matching_products = Product.objects.filter(
                        marketplaceproduct__marketplace_id__in=marketplaces_list
                    ).distinct()
                    parent_ids = matching_products.values_list("parent", flat=True)
                    queryset = queryset.filter(
                        Q(id__in=matching_products.values_list("id", flat=True)) |
                        Q(id__in=parent_ids)
                    )

        if paginated:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



# from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

# from django.db.models import Q

# from .models import Product, ProductAttribute, ProductAttributeType

# from .serializers import ProductParentMinimalSerializer, ProductSerializer, ProductAttributeSerializer, ProductAttributeTypeSerializer
# from .pagination import ProductPagination

# from itertools import chain

# class ProductListView(ListAPIView):
#     queryset = Product.objects.filter(parent__isnull=True).order_by("id")
#     serializer_class = ProductParentMinimalSerializer
#     pagination_class = ProductPagination

#     def get_queryset(self):
#         queryset = super().get_queryset()

#         marketplaces = self.request.query_params.get("marketplace")
#         search = self.request.query_params.get("search")

#         if not marketplaces:
#             return queryset.none()

#         if search:
#             matching_products = Product.objects.filter(
#                 Q(name__icontains=search) |
#                 Q(sku__icontains=search) |
#                 Q(reference__icontains=search)
#             )
#             parent_ids = matching_products.values_list("parent", flat=True)
#             queryset = queryset.filter(
#                 Q(id__in=matching_products.values_list("id", flat=True)) |
#                 Q(id__in=parent_ids)
#             )

#         marketplaces_list = marketplaces.split(",")

#         if "0" in marketplaces_list:
#             filter_conditions = Q(marketplaceproduct__marketplace_id__in=marketplaces_list) | (Q(marketplaceproduct__isnull=True) & Q(children__isnull=True))
#         else:
#             filter_conditions = Q(marketplaceproduct__marketplace_id__in=marketplaces_list)

#         matching_products_with_marketplace = Product.objects.filter(filter_conditions).values_list("id", "parent")

#         product_ids = set(chain(*matching_products_with_marketplace))

#         queryset = queryset.filter(id__in=product_ids)

#         return queryset

# class ProductView(RetrieveUpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class ProductAttributeListView(ListAPIView):
#     queryset = ProductAttribute.objects.all()
#     serializer_class = ProductAttributeSerializer

# class ProductAttributeTypeListView(ListAPIView):
#     queryset = ProductAttributeType.objects.all()
#     serializer_class = ProductAttributeTypeSerializer
