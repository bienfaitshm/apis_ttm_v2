from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings


class PostAction:
    def post_action(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, *args, **kwargs)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListAction:
    def list_action(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # type: ignore

        page = self.paginate_queryset(queryset)  # type: ignore
        if page is not None:
            serializer = self.get_serializer(page, many=True)  # type: ignore
            return self.get_paginated_response(serializer.data)  # type: ignore

        serializer = self.get_serializer(queryset, many=True)  # type: ignore
        return Response(serializer.data)
