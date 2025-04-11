from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"marketplaces", views.MarketplaceViewSet, basename="marketplace")

urlpatterns = router.urls