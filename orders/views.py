from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from .pagination import OrderPagination

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request):
        queryset = self.get_queryset()
        customer_ids = request.query_params.get("customer_ids")

        if customer_ids:
            try:
                ids = [int(customer_id) for customer_id in customer_ids.split(",")]
                queryset = queryset.filter(id__in=ids)
            except ValueError:
                return Response({"error": "Invalid customer_ids parameter"}, status=400)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     paginated = request.query_params.get("paginated", "false").lower() == "true"

    #     if paginated:
    #         paginator = PageNumberPagination()
    #         page = paginator.paginate_queryset(queryset, request)
    #         if page is not None:
    #             serializer = self.get_serializer(page, many=True)
    #             return paginator.get_paginated_response(serializer.data)
            
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)


# from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework import filters

# from .models import Order

# from .serializers import OrderMinimalSerializer, OrderSerializer
# from .pagination import OrderPagination

# class OrderListView(ListAPIView):
#     search_fields = ["order_id", "ticket", "customer__bill_firstname", "customer__bill_lastname"]
#     filter_backends = (filters.SearchFilter,)
#     queryset = Order.objects.order_by("-order_date")
#     serializer_class = OrderMinimalSerializer
#     pagination_class = OrderPagination

#     def get_queryset(self):
#         queryset = super().get_queryset()

#         marketplaces = self.request.query_params.get("marketplace")

#         if not marketplaces:
#             return queryset.none()
    
#         marketplaces_list = marketplaces.split(",")
#         queryset = queryset.filter(marketplace_id__in=marketplaces_list)

#         return queryset

# class OrderView(RetrieveUpdateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer