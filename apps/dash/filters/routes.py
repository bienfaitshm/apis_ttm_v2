from rest_framework.compat import coreapi, coreschema
from django.utils.encoding import force_str

from rest_framework import filters

from apps.dash.process.tarif import get_tarif_of_route
from ..process.routes import RouteProcess


class FilterRouteType(filters.BaseFilterBackend):
    route_name = "type"

    def filter_queryset(self, request, queryset, view):
        qs = queryset
        _type = request.query_params.get(self.route_name)
        if _type == "depart":
            qs = qs.filter(whereFrom=None)
        if _type == "destination":
            qs = qs.filter(whereTo=None)
        return qs

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name="type",
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str("type"),
                    format="all | depart | destination",
                    description=force_str(
                        "deternime type of route, default is `all`, type can be [all, depart, destination]")
                )
            ),
        ]
