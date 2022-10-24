
from rest_framework import serializers


class ChainRouteItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    origin = serializers.IntegerField(source="origin.pk")
    town = serializers.CharField(source="node.town")
    code = serializers.CharField(source="node.code")
    whereFrom = serializers.IntegerField(
        source="whereFrom.pk",
        required=False,
        default=None
    )
    whereTo = serializers.IntegerField(
        source="whereTo.pk",
        required=False,
        default=None
    )
    level = serializers.IntegerField()


class ChainRouteSerializers(serializers.Serializer):
    where_from = ChainRouteItemSerializer(required=False, default=None)
    where_to = ChainRouteItemSerializer(required=False, default=None)
    scales = ChainRouteItemSerializer(many=True)
    has_scales = serializers.BooleanField(default=False)  # type: ignore
