
import random
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from apps.clients.models import SeletectedJourney
from apps.clients.selectors import selector_reservation as SR


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
        assert self.OutputSerializer is not None, (
            "'%s' should either include a `OutputSerializer` attribute, "
            % self.__class__.__name__
        )
        return self.OutputSerializer


class DashViewReservation(GenericMixinView, generics.ListAPIView):
    class OutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = SeletectedJourney
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
            model = SeletectedJourney
            fields = ("id", "status", "pnr", "folder", "n_folder",
                      "client_full_name", "date_created", )

    def get_queryset(self):
        return SR.get_dash_detail_reservation()
