from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"customers", views.CustomerViewSet, basename="customer")
router.register(r"orders", views.OrderViewSet, basename="order")

urlpatterns = router.urls