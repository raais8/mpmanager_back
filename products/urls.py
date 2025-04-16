from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"products", views.ProductViewSet, basename="product")

urlpatterns = router.urls

# app_name = 'products'
# urlpatterns = [
#     path('api/product-list/', views.ProductListView.as_view(), name='product_list'),
#     path('api/product/<int:pk>', views.ProductView.as_view(), name='product'),
#     path('api/product-attribute-list/', views.ProductAttributeListView.as_view(), name='product_attribute_list'),
#     path('api/product-attribute-type-list/', views.ProductAttributeTypeListView.as_view(), name='product_attribute_type_list'),
# ]