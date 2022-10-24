
from rest_framework import pagination, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.clients.selectors.infos_reservations import reservation_progression
from apps.clients.selectors.search import search_selector
from apps.clients.serializers import serialzers as sr
from apps.clients.services import reservations_services as r_service
from apps.dash import models as dash_model
from apps.dash.services import routes
from utils import rest_actions

register_serializers = {
    "search": sr.RSearchSerializer,
    "select_reservation": sr.RSelectSerializer,
    "passengers": sr.RPassengerSerializer,
    "other_info": sr.R_OtherInfoSerializer,
    "complete": sr.RCompletedSerializer,
    "progression": sr.ProgressionInfoSerializer
}


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': len(data),
            'results': data
        })


class ReservationViewApis(
    rest_actions.PostAction,
    rest_actions.ListAction,
    viewsets.GenericViewSet
):
    """
    reservations actions
    params
        adult:1
        baby:0
        child:0
        dateDepature: ""
        journeyClass:""
        whereFrom:""
        whereTo:"bienfait"
    """
    pagination_class = CustomPagination
    serializer_class = sr.RSearchSerializer
    queryset = dash_model.Journey.objects.all()

    def get_data(self):
        params: dict = {}
        if hasattr(self.request, "query_params"):
            params = self.request.query_params  # type: ignore
        return list(search_selector(self.queryset, **params))

    def get_serializer_class(self, *args, **kwargs):
        return register_serializers.get(self.action, self.serializer_class)

    @action(detail=True, name="Reservation Progression")
    def progression(self, request, pk):
        success, value = reservation_progression(session=pk)
        if success:
            serializer = self.get_serializer(value)
            return Response(serializer.data)
        return Response({"detail": value}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, name="Search journey")
    def search(self, request):
        return self.list_action(request)

    @action(detail=False, methods=["post"], name="Select journey")
    def select_reservation(self, request):
        """ select the reservation """
        return self.post_action(request)

    @action(detail=True, methods=["post"], name="Reservation Passenger")
    def passengers(self, request, pk):
        """ create list of passenger in the reservation """
        return self.post_action(request, pk=pk)

    @action(
        detail=True,
        methods=["post"],
        name="Other info (detail information)"
    )
    def other_info(self, request, pk):
        """ adding the other information in the reservation"""
        return self.post_action(request, pk=pk)

    @action(detail=True, methods=["get"], name="Servation Complted")
    def complete(self, request, pk):
        """ get and check if the reservation is finiched"""
        reservation = r_service.ReservationServices(session=pk)
        data = self.get_serializer(reservation.get_completed()).data
        return Response(data, status=status.HTTP_200_OK)
