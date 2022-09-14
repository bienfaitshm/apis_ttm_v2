from typing import Any, Dict

from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.clients.process.search import SearchProcess
from apps.clients.process.selectors import get_tarif_for_a_reservation
from apps.clients.serializers.serialzers import (
    OtherInfoReservationSerializer, PassengerSerializer,
)
from apps.clients.services.reservations_services import (
    add_other_info, add_passengers, create_reservation,
)
from apps.dash.models.transport import Journey
from apps.dash.process import routes
from apps.dash.serializers.serializers import JourneyTarifSerializer
from utils import fields

from ..models import ResearchReservation, SeletectedJourney

default_device = ["USD", "CDF"]


class JPassengersDataSerializer(serializers.Serializer):
    adult = serializers.IntegerField(default=settings.ADULT)
    child = serializers.IntegerField(default=settings.CHILD)
    inf = serializers.IntegerField(default=settings.INF)


class JReservationSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    where_from = serializers.CharField()
    where_to = serializers.CharField()
    datetime_from = serializers.DateTimeField()
    datetime_to = serializers.DateTimeField()
    duration = serializers.DateTimeField()
    passengers = JPassengersDataSerializer()
    j_class = serializers.CharField()
    total_price = serializers.FloatField()
    device = serializers.ChoiceField(choices=default_device, default="USD")
    has_scale = serializers.BooleanField(default=False)  # type: ignore
    scales = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    message = serializers.CharField(required=False)
    is_selected_for = serializers.BooleanField(default=False)  # type: ignore
    is_expired = serializers.BooleanField(default=False)  # type: ignore


class ReachercheJourneyReservationSerializer(serializers.ModelSerializer):
    journies = serializers.SerializerMethodField(method_name="get_journies")

    class Meta:
        model = ResearchReservation
        # depth = 1
        fields = "__all__"
        extra_kwargs = {
            'journey_class': {'required': True, "allow_null": False},
            'whereFrom': {'required': True, "allow_null": False},
            'whereTo': {'required': True, "allow_null": False}
        }

    def get_journies(self, objt):
        return SearchProcess.search(objt)


class SelectjourneyReservation(serializers.ModelSerializer):
    tarif = serializers.SerializerMethodField(
        method_name="get_tarif", read_only=True)
    session_key = serializers.CharField(source="session.key", read_only=True)
    date_expiration = serializers.CharField(
        source="session.date_expiration", read_only=True)
    code_folder = serializers.CharField(source="folder.number", read_only=True)
    cars = serializers.CharField(source="cars.codeAppareil", read_only=True)
    info = serializers.SerializerMethodField(method_name="get_info")

    class Meta:
        model = SeletectedJourney
        # depth = 2
        exclude = ['folder', 'session']
        read_only_fields = ['session', 'folder', 'state', "pnr"]
        extra_kwargs = {
            'journey_class': {'required': True, "allow_null": False}
        }

    def create(self, validated_data: dict):
        """ create a new reservation """
        # validated_data.pop("pnr")
        print(validated_data)
        journey = validated_data.pop("journey")
        return create_reservation(journey=journey, **validated_data)
        # reservation = ReservationJourney()
        # return reservation.select_journey(**validated_data)

    def get_tarif(self, objet: object) -> object:
        tarif = get_tarif_for_a_reservation(
            route=objet.journey.route, journey_class=objet.journey_class)
        return JourneyTarifSerializer(tarif).data

    def get_info(self, objet: SeletectedJourney):
        """  Voyage <b>234 n0 1234</b> dimanche 19 decembre 2021
        - Depart Kinshasa N'Djili a 08:00 - Arrivee Goma a
        11:20 """
        journey: Journey = objet.journey
        depart = routes.RouteProcess.first(journey.route)
        destination = journey.route.node
        message = [_("Voyage n")]
        # number of journey
        message.append(_(journey.numJourney))

        message.extend(
            (_(journey.dateDeparture.strftime("%A %d %B %Y")), " - Depart a"))

        if depart:
            message.append(depart.town)

        message.extend(
            (journey.hoursDeparture.strftime("%H:%M"), "- Arrivee "))
        message.append(destination.town)
        # time arrive
        message.append(journey.hoursReturn.strftime("%H:%M"))

        return _(" ".join(message))


class PassengerJourneyReservation(serializers.Serializer):
    session = fields.SessionField(
        required=True, write_only=True,
        queryset=SeletectedJourney.objects.all()
    )
    passengers = PassengerSerializer(many=True)

    def create(self, validated_data: dict):
        passengers: list = validated_data.get("passengers")
        session = validated_data.get("session")

        _passenger = add_passengers(
            jouney=session, passengers=passengers)
        return {"passengers": _passenger}


class OtherInfoJourneyReservation(serializers.Serializer):
    session = fields.SessionField(
        required=True, write_only=True,
        queryset=SeletectedJourney.objects.all()
    )
    other_info = OtherInfoReservationSerializer()

    def create(self, validated_data: Dict[str, Any]):
        other_info: list = validated_data.get("other_info")
        session = validated_data.get("session")
        _other_info = add_other_info(
            journey=session, other_info=other_info)

        return {"other_info": _other_info}
