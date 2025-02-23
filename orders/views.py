from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import filters

from .models import Order

from .serializers import OrderListSerializer
from .pagination import OrderPagination

class OrderListView(ListAPIView):
    search_fields = ["order_id", "ticket"]
    filter_backends = (filters.SearchFilter,)
    queryset = Order.objects.order_by("-order_date")
    serializer_class = OrderListSerializer
    pagination_class = OrderPagination