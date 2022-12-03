from rest_framework import serializers

from ..models import Passenger


class SplitFolderSerialiser(serializers.Serializer):
    passengers = serializers.PrimaryKeyRelatedField(
        queryset=Passenger.objects.all(), write_only=True)

    def create(self, validated_data):
        return super().create(validated_data)


class DownloadTicketSerializer(serializers.Serializer):
    file = serializers.FileField(required=None, default=None)
