from rest_framework import generics
from ..serializers.reservation import SelectjourneyReservation
from ..models import SeletectedJourney


class SelectJourneyreservationView(generics.CreateAPIView):
    queryset = SeletectedJourney.objects.all()
    serializer_class = SelectjourneyReservation
