
from rest_framework import serializers
from apps.dash.process.routes import RouteProcess
from apps.dash.process.tarif import get_tarif_of_route

from apps.dash.serializers.type import JourneyDataType
from ..models.technique import Cars, Seat, CabinePlane
from ..models.transport import (
    CoverCity, Journey, JourneyClass, JourneyTarif, PointOfSale, Routing, PointOfSaleWorker
)


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = "__all__"


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"
        read_only_fields = ['idConfigCab']


class CabinePlaneSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True)

    class Meta:
        model = CabinePlane
        fields = "__all__"

    def create(self, validated_data):
        seats_data = validated_data.pop('seats')
        cabine_config = CabinePlane.objects.create(**validated_data)
        #
        seats = [Seat(**i, idConfigCab=cabine_config) for i in seats_data]
        Seat.objects.bulk_create(seats)
        return cabine_config


class CoverCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverCity
        fields = "__all__"


class PointOfSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfSale
        fields = "__all__"


class RoutingProcessSerializer(serializers.ModelSerializer):
    whereTo = serializers.SerializerMethodField(method_name="get_next")

    class Meta:
        model = Routing
        fields = "__all__"

    def get_next(self, obj: Routing):
        if obj.whereTo is None:
            return None
        return RoutingProcessSerializer(obj.whereTo).data


class RoutingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routing
        fields = "__all__"

    def create(self, validated_data):
        return RouteProcess.create(**validated_data)


class RoutingMoreInfoSerializer(serializers.ModelSerializer):
    whereFromTown = serializers.SerializerMethodField(method_name="get_depart")
    whereToTown = serializers.SerializerMethodField(
        method_name="get_destination")
    escales = serializers.SerializerMethodField(method_name="get_escales")
    last_route = serializers.SerializerMethodField(
        method_name="get_last_route")

    class Meta:
        model = Routing
        fields = "__all__"

    def get_last_route(self, obj):
        return RouteProcess.last_route(obj).pk

    def get_depart(self, obj: Routing):
        if route := RouteProcess.first(obj):
            return CoverCitySerializer(instance=route).data

    def get_destination(self, obj: Routing):
        if route := RouteProcess.last(obj):
            return CoverCitySerializer(instance=route).data

    def get_escales(self, obj: Routing):
        escales = RouteProcess.get_scale(obj)
        return CoverCitySerializer(instance=escales, many=True).data


class PointOfSaleWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfSaleWorker
        fields = "__all__"


class JourneySerializer(serializers.ModelSerializer):
    direct = serializers.SerializerMethodField(method_name="get_is_direct")

    class Meta:
        model = Journey
        fields = "__all__"
        extra_kwargs = {
            'route': {'required': True, "allow_null": False}
        }

    def get_is_direct(self, obj: Journey):
        return RouteProcess.number_of_escale(obj.route) <= 0

    def validate_route(self, value: Journey):
        if RouteProcess.is_last_route(value):
            return value
        raise serializers.ValidationError(
            "Route is not destination, please affect destination route to the journey")


class JourneyMoreInfoSerializer(JourneySerializer):
    route = RoutingMoreInfoSerializer()
    scales = serializers.SerializerMethodField(method_name="get_escales")
    depart = serializers.SerializerMethodField(method_name="get_depart")
    destination = serializers.SerializerMethodField(
        method_name="get_destination")
    tarif = serializers.SerializerMethodField(
        method_name="get_tarif")

    class Meta(JourneySerializer.Meta):
        pass

    def get_tarif(self, obj: Journey):
        return JourneyTarifSerializer(instance=get_tarif_of_route(obj.route), many=True).data

    def get_depart(self, obj: Journey):
        return CoverCitySerializer(instance=RouteProcess.first(obj.route)).data

    def get_destination(self, obj: Journey):
        if hasattr(obj.route, "node") and obj.route.node:
            return CoverCitySerializer(instance=obj.route.node).data

    def get_escales(self, obj: Journey):
        escales = RouteProcess.get_scale(obj.route)
        return CoverCitySerializer(instance=escales, many=True).data


class JourneyClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyClass
        fields = "__all__"


class JourneyTarifSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(
        source="journey_class.name", read_only=True)

    class Meta:
        model = JourneyTarif
        fields = "__all__"

    def validate_route(self, value: Journey):
        if RouteProcess.is_last_route(value):
            return value
        raise serializers.ValidationError(
            "Route is not destination, select a destination route for affecting a tarif")
