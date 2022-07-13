from rest_framework import generics, serializers, status
from rest_framework.response import Response
from apps.clients.models import JourneyClientFolder, Passenger
from apps.clients.process.reservation import ReservationJourney
from apps.clients.serializers.serialzers import SeletectedJourneySerializer


class SplitFolderView(generics.GenericAPIView):
    class SpliteSerializer(serializers.Serializer):
        reservation = serializers.PrimaryKeyRelatedField(
            queryset=JourneyClientFolder.objects.all())
        passengers = serializers.PrimaryKeyRelatedField(
            queryset=Passenger.objects.all(), write_only=True, many=True)

    def get_serializer_class(self):
        return self.SpliteSerializer

    def post(self, request):
        data = self.SpliteSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        res_objt = ReservationJourney()
        passengers = data.validated_data.get("passengers")
        reservation = data.validated_data.get("reservation")
        responce = res_objt.splite_reservation(
            reservation=reservation, passengers=passengers)
        return Response(SeletectedJourneySerializer(responce).data, status=status.HTTP_201_CREATED)


class VoidSelectedJourneyView(generics.GenericAPIView):
    def delete(self, request, id, *args, **kwargs):
        reservation = ReservationJourney()
        responce = reservation.void(reservation=id)
        return Response({"status": responce}, status=status.HTTP_200_OK)


class ChangeRoutingSelectedJourneyView:
    pass
