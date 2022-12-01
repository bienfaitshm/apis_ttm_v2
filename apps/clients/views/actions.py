from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, generics, serializers, status
from rest_framework.response import Response

from apps.clients.models import Passenger, Reservation
from apps.clients.serializers.serialzers import SeletectedJourneySerializer
from apps.clients.services.reservations_services import (
    splite_reservation, void_reservation,
)

SERVER_ERROR_MESSAGE = """
    There in a error on splite the reservation from Apis, please try later!
"""


def get_reservation_queryset() -> QuerySet[Reservation]:
    return Reservation.objects.all()\
        .select_related("other_info", "session")


def get_passengers_queryset() -> QuerySet[Passenger]:
    return Passenger.objects.all()


class SplitFolderView(generics.GenericAPIView):
    class SpliteSerializer(serializers.Serializer):
        reservation = serializers.PrimaryKeyRelatedField(
            queryset=get_reservation_queryset())
        passengers = serializers.PrimaryKeyRelatedField(
            queryset=get_passengers_queryset(), write_only=True, many=True)

    def get_serializer_class(self):
        return self.SpliteSerializer

    def post(self, request):
        data = self.SpliteSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        passengers = data.validated_data.get("passengers", [])
        reservation = data.validated_data.get("reservation")

        responce = splite_reservation(
            reservation=reservation, passengers=passengers)

        # error on splite reservation
        if not responce:
            raise exceptions.APIException(
                _(SERVER_ERROR_MESSAGE)
            )

        # base reauest
        code, value = responce
        if code == "error":
            raise exceptions.APIException(
                value, code=status.HTTP_400_BAD_REQUEST)

        responce = SeletectedJourneySerializer(value).data
        return Response(responce, status=status.HTTP_201_CREATED)


class VoidSelectedJourneyView(generics.GenericAPIView):
    def delete(self, request, id, *args, **kwargs):
        responce = void_reservation(reservation=id)
        return Response({"status": responce}, status=status.HTTP_200_OK)
