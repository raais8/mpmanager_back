from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import filters

from .models import Order

from .serializers import OrderMinimalSerializer, OrderSerializer
from .pagination import OrderPagination

class OrderListView(ListAPIView):
    search_fields = ["order_id", "ticket", "customer__bill_firstname", "customer__bill_lastname"]
    filter_backends = (filters.SearchFilter,)
    queryset = Order.objects.order_by("-order_date")
    serializer_class = OrderMinimalSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        marketplaces = self.request.query_params.get("marketplace")

        if not marketplaces:
            return queryset.none()
    
        marketplaces_list = marketplaces.split(",")
        queryset = queryset.filter(marketplace_id__in=marketplaces_list)

        return queryset

class OrderView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer