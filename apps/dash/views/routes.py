from rest_framework import viewsets
from rest_framework.response import Response

from apps.dash.serializers.serializers import RoutingProcessSerializer
from ..models import Routing


class RouteProcessView(viewsets.ReadOnlyModelViewSet):
    queryset = Routing.objects.all()
    permission_classes = []
    serializer_class = RoutingProcessSerializer

    def get_queryset(self):
        return super().get_queryset().filter(whereFrom=None)
