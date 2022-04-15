from rest_framework import serializers
from apps.dash.models import JourneyClass

from ..models import SeletectedJourney
from ..process.reservation import ReservationJourney


class SelectjourneyReservation(serializers.ModelSerializer):
    info = serializers.SerializerMethodField(
        method_name="get_info", read_only=True)
    session_key = serializers.CharField(source="session.key", read_only=True)
    journey_class = serializers.PrimaryKeyRelatedField(
        queryset=JourneyClass.objects.all(), write_only=True)

    class Meta:
        model = SeletectedJourney
        fields = "__all__"
        read_only_fields = ['session', 'folder', 'session_key']
        extra_kwargs = {
            'journey_class': {'write_only': True}
        }

    def create(self, validated_data: dict):
        self.tmp = validated_data.pop("journey_class")
        return ReservationJourney.select_journey(**validated_data)

    def get_info(self, objet):
        return str(self.tmp)
