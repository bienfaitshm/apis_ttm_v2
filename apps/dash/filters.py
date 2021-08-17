from rest_framework import filters
from rest_framework.compat import coreapi, coreschema, distinct
from django.utils.encoding import force_str


class IsComponyFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    params_company = 'company'

    def filter_queryset(self, request, queryset, view):
        company = request.query_params.get(self.params_company)
        if company:
            return queryset.filter(company=company)
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': self.params_company,
                'required': False,
                'in': 'query',
                'description': "return only data of campany (pk of campany)",
                'schema': {
                    'type': 'string',
                },
            },
        ]

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.params_company,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str("Company"),
                    description=force_str(
                        "return only data of campany (pk of campany)")
                )
            )
        ]


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class SearchJourneyFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        # onlyDirect, whereFrom, whreTo, dateDeparture, dateReturn, hoursDeparture, hoursReturn
        # onlyDirect
        company = request.query_params.get('company')
        return queryset


class SearchWhereFromToFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        whereFrom = request.query_params.get('whereFrom')
        if whereFrom:
            queryset = queryset.filter(routing__whereFrom__town__icontains=whereFrom)
        whreTo = request.query_params.get('whreTo')
        if whreTo:
            queryset = queryset.filter(routing__whreTo__town__icontains=whereFrom)
        return queryset

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name="whereFrom",
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str("whereFrom"),
                    description=force_str(
                        "town of comming from")
                )
            ),
            coreapi.Field(
                name="whreTo",
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str("whreTo"),
                    description=force_str(
                        "town we want go")
                )
            )
        ]
