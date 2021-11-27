from rest_framework import serializers
from .models.technique import Cars, Seat, CabinePlane
from .models.transport import (
    CoverCity, Journey, PointOfSale, Routing, PointOfSaleWorker, RouteJourney
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


class RouteJourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteJourney
        fields = "__all__"

class RoutingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routing
        fields = "__all__"


class RoutingMoreInfoSerializer(serializers.ModelSerializer):
    whereFrom = serializers.CharField(source="whereFrom.town")
    whereTo = serializers.CharField(source="whereTo.town")
    class Meta:
        model = Routing
        fields = "__all__"


class PointOfSaleWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfSaleWorker
        fields = "__all__"
        

class JourneySerializer(serializers.ModelSerializer):
    direct = serializers.BooleanField(source="is_direct", default=False, read_only=True)
    journey_routes = RouteJourneySerializer(many=True)
    class Meta:
        model = Journey
        fields = "__all__"


class JourneyMoreInfoSerializer(JourneySerializer):
    routes = RoutingMoreInfoSerializer(many=True)
    class Meta(JourneySerializer.Meta):
        pass
    
    def is_direct(self, instance):
        print("is_direct :", instance.is_direct)
        return True
