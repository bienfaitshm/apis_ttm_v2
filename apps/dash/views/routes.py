from rest_framework import viewsets
from rest_framework.response import Response

from apps.dash.serializers.serializers import RoutingProcessSerializer
from ..models import Routing


class RouteProcessView(viewsets.ViewSet):
    queryset = Routing.objects.all()
    permission_classes = []
    serializer_class = RoutingProcessSerializer

    def list(self, request, *args, **kwargs):

        return Response({
            "data": "ok",
            "list": str(self.first())
        })

    def create(self, request, *args, **kwargs):
        return Response({
            "d": "created"
        })

    def first(self):
        qs: Routing = self.queryset.get(pk=1)
        last = None
        current = qs
        while current != None:
            last = current.node
            current = current.whereTo
        return last
