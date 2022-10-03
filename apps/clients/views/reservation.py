from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.clients.selectors import selector_reservation
from apps.clients.serializers import serialzers as sr
from apps.clients.services import reservations_services as r_service
from utils import rest_actions

register_serializers = {
    "search": sr.RSearchSerializer,
    "select_reservation": sr.RSelectSerializer,
    "passengers": sr.RPassengerSerializer,
    "other_info": sr.R_OtherInfoSerializer,
    "complete": sr.RCompletedSerializer,
}


class ReservationViewApis(rest_actions.PostAction,
                          rest_actions.ListAction,
                          viewsets.GenericViewSet):
    """
    reservations actions
    """
    serializer_class = sr.RSearchSerializer

    def get_serializer_class(self, *args, **kwargs):
        return register_serializers.get(self.action, self.serializer_class)

    def get_queryset(self):
        return selector_reservation.find_reservation_journey()

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(session=kwargs.get("pk"))

    def progession(self, request, session):
        return Response({})

    @action(detail=False, name="Search journey")
    def search(self, request):
        return self.list_action(request)

    @action(detail=False, methods=["post"], name="Select journey")
    def select_reservation(self, request):
        return self.post_action(request)

    @action(detail=True, methods=["post"], name="Reservation Passenger")
    def passengers(self, request, pk):
        return self.post_action(request, pk=pk)

    @action(
        detail=True,
        methods=["post"],
        name="Other info (detail information)"
    )
    def other_info(self, request, pk):
        return self.post_action(request, pk=pk)

    @action(detail=True, methods=["get"], name="Servation Complted")
    def complete(self, request, pk):
        reservation = r_service.ReservationServices(session=pk)
        data = self.get_serializer(reservation.get_completed()).data
        return Response(data, status=status.HTTP_200_OK)
