from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.clients.selectors import search, selector_reservation
from apps.clients.serializers import serialzers as sr
from apps.clients.services import reservations_services as r_service
from apps.dash import models as dash_model
from utils import rest_actions

register_serializers = {
    "search": sr.RSearchSerializer,
    "select_reservation": sr.RSelectSerializer,
    "passengers": sr.RPassengerSerializer,
    "other_info": sr.R_OtherInfoSerializer,
    "complete": sr.RCompletedSerializer,
}


class ReservationViewApis(
    rest_actions.PostAction,
    rest_actions.ListAction,
    viewsets.GenericViewSet
):
    """
    reservations actions
    """
    serializer_class = sr.RSearchSerializer
    queryset = dash_model.Journey.objects.all()

    def get_queryset(self):
        return search.SearchSelector(self.queryset).get_search()

    def get_serializer_class(self, *args, **kwargs):
        return register_serializers.get(self.action, self.serializer_class)

    def progression(self, request, session):
        return Response({})

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
