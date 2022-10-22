from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.dash.serializers.routes import ChainRouteSerializers
from apps.dash.services.routes import Routes

from ..models import Routing


class RouteProcessView(viewsets.GenericViewSet):
    queryset = Routing.objects.all()
    permission_classes = []
    serializer_class = ChainRouteSerializers

    def list(self, request):
        _routes = Routes()
        serializers = ChainRouteSerializers(
            _routes.get_routes_data(), many=True
        )
        return Response(serializers.data)
