
import random

from rest_framework import generics, serializers

from apps.clients.models import Reservation
from apps.clients.selectors import selector_reservation as SR
from apps.dash.models.transport import Journey
from apps.dash.selectors.finder import finder_journey

# from rest_framework.response import Response


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(
        name=str(random.randint(1234, 9999)), fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)
    return serializer_class(**kwargs)


class GenericMixinView:
    def get_serializer_class(self):
        assert self.OutputSerializer is not None, (  # type: ignore
            "'%s' should either include a `OutputSerializer` attribute, "
            % self.__class__.__name__
        )
        return self.OutputSerializer  # type: ignore


class JourneyFinder(GenericMixinView, generics.ListAPIView):
    """
    finder of journey
    `bienfait`\n
    Args:
        GenericMixinView (_type_): _description_
        generics (_type_): _description_

    Returns:
        _type_: _description_
    """
    class OutputSerializer(serializers.ModelSerializer):

        sugestion = serializers.BooleanField(
            default=False,  # type: ignore
            help_text="the sugestion search"
        )
        direct = serializers.BooleanField(
            default=False,  # type: ignore
            help_text="journey with scale or no scale"
        )

        whereFromName = serializers.CharField(
            default=None,
            help_text="the name where the journey comming from"
        )

        whereToName = serializers.CharField(
            default=None,
            help_text="the name where the journey comming from"
        )

        class Meta:
            model = Journey
            fields = [
                "id",
                "dateDeparture",
                "hoursDeparture",
                "whereFromName",
                "whereToName",
                "numJourney",
                # "exprired",
                "sugestion",
                "direct"
            ]
            ref_name = "finder_journey"

    def get_queryset(self):
        return finder_journey()


class DashViewReservation(GenericMixinView, generics.ListAPIView):
    class OutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = Reservation
            fields = ("id", "status",)
            ref_name = "OutputSerializerDetail"

    def get_queryset(self):
        return SR.get_dash_reservations()


class DashViewDetailReservation(GenericMixinView, generics.RetrieveAPIView):
    lookup_field = "id"

    class OutputSerializer(serializers.ModelSerializer):
        client_full_name = serializers.CharField()
        n_folder = serializers.CharField()
        passengers = inline_serializer(many=True, fields={
            'id': serializers.IntegerField(),
            "firstname": serializers.CharField(),
            'middlename': serializers.CharField(),
            'lastname': serializers.CharField()
        })

        class Meta:
            ref_name = "OutputSerializerDetail"
            model = Reservation
            fields = ("id", "status", "pnr", "folder", "n_folder",
                      "client_full_name", "date_created", )

    def get_queryset(self):
        return SR.get_dash_detail_reservation()
