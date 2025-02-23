from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Marketplace

from .serializers import MarketplaceSerializer

class MarketplaceListView(APIView):
    def get(self, request):
        marketplaces = Marketplace.objects.all()
        serializer = MarketplaceSerializer(marketplaces, many=True)
        return Response(serializer.data)
