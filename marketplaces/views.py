from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Marketplace

from .serializers import MarketplaceSerializer

class MarketplaceListView(ListAPIView):
    queryset = Marketplace.objects.all().order_by("name")
    serializer_class = MarketplaceSerializer