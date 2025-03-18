from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('api/product-list/', views.ProductListView.as_view(), name='product_list'),
]