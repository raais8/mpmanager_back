from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Marketplace
from .serializers import MarketplaceSerializer

class MarketplaceViewSet(ModelViewSet):
    queryset = Marketplace.objects.all().order_by("name")
    serializer_class = MarketplaceSerializer

    def list(self, request):
        queryset = self.get_queryset()
        marketplace_ids = request.query_params.get("marketplace_ids")

        if marketplace_ids:
            try:
                ids = [int(marketplace_id) for marketplace_id in marketplace_ids.split(",")]
                queryset = queryset.filter(id__in=ids)
            except ValueError:
                return Response({"error": "Invalid marketplace_ids parameter"}, status=400)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)