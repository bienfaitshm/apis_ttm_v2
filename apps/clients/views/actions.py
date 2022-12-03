from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, generics, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.clients.models import Passenger, Reservation
from apps.clients.reverse_url_names import ActionUrlPathName
from apps.clients.serializers.actions import DownloadTicketSerializer
from apps.clients.serializers.serialzers import SeletectedJourneySerializer
from apps.clients.services.reservations_services import (
    splite_reservation, void_reservation,
)
from systen.pdf_render import (
    InfoReservationPdf, PassengersPdf, render_pdf_view, template_render,
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


# serializers dictionary
serializer_dict = {
    # download serializer ticket as pdf
    ActionUrlPathName.DOWNLOAD_TICKET: DownloadTicketSerializer
}


class ActionViewApis(viewsets.GenericViewSet):
    serializer_classes: dict = serializer_dict
    default_key_serializer: str = ActionUrlPathName.DOWNLOAD_TICKET

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_classes.get(self.action, self.default_key_serializer)

    @action(
        detail=True,
        methods=["post"],
        name="download ticket as pdf",
        # url_name=ActionUrlPathName.DOWNLOAD_TICKET
    )
    def download_ticket(self, request, *args, **kwargs):
        psg = []
        for p in range(1):
            pp = PassengersPdf(
                birth_date="23/03/1995",
                devise="DCF",
                name="Mr Kilumba shomari",
                taxe=p,
                taxe_price=456,
                total_price=2345,
                unit_price=234,
                user_type="AD"
            )
            psg.append(pp)

        html = template_render(InfoReservationPdf(
            pnr="123EROK",
            devise="CDF",
            expired_end_date="Samedi, Le 30/12/2022",
            passengers=psg,
            reservation_date="date",
        ))

        return render_pdf_view(request=request, html=html)
