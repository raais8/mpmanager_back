from rest_framework.pagination import PageNumberPagination

class OrderPagination(PageNumberPagination):
    page_size = 25
    page_query_param = "page"
    page_size_query_param = "limit"
    max_page_size = 100