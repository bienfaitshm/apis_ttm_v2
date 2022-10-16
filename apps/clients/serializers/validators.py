from rest_framework import serializers

from apps.dash.models import Journey


def journey_expired_validator(value):
    # if value.exprired:
    #     raise serializers.ValidationError("Journy selected is expired")
    pass
