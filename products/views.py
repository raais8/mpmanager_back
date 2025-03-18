from rest_framework.generics import ListAPIView

from .models import Product

from .serializers import ProductParentMinimalSerializer
from .pagination import ProductPagination

class ProductListView(ListAPIView):
    queryset = Product.objects.filter(parent__isnull=True)
    serializer_class = ProductParentMinimalSerializer
    pagination_class = ProductPagination

