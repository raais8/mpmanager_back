from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('api/order-list/', views.OrderListView.as_view(), name='order_list'),
    path('api/order/<int:pk>', views.OrderView.as_view(), name='order'),
]