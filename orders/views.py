from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Customer, Order, OrderItem
from .serializers import CustomerSerializer, OrderSerializer, OrderItemSerializer
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
    search_fields = ["order_id", "ticket", "customer__bill_firstname", "customer__bill_lastname"]
    filter_backends = (filters.SearchFilter,)

    def list(self, request):
        queryset = self.get_queryset()
        marketplace_ids = request.query_params.get("marketplace_ids")

        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)

        if marketplace_ids:
            try:
                ids = [int(marketplace_id) for marketplace_id in marketplace_ids.split(",")]
                queryset = queryset.filter(marketplace_id__in=ids)
            except ValueError:
                return Response({"error": "Invalid marketplace_ids parameter"}, status=400)
        else:
            queryset = queryset.none()
            
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def list(self, request):
        queryset = self.get_queryset()
        order_id = request.query_params.get("order_id")

        if order_id:
            try:
                order_id = int(order_id)
                queryset = queryset.filter(order_id=order_id)
            except ValueError:
                return Response({"error": "Invalid order_id parameter"}, status=400)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # CREATE MULTIPLE ORDER ITEMS WITH A SINGLE REQUEST
    # def create(self, request, *args, **kwargs):
    #     is_many = isinstance(request.data, list)

    #     serializer = self.get_serializer(data=request.data, many=is_many)
    #     serializer.is_valid(raise_exception=True)

    #     if is_many:
    #         serializer.save()
    #     else:
    #         self.perform_create(serializer)

    #     return Response(serializer.data, status=201)








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