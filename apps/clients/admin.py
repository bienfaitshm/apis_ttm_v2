from django.contrib import admin
from .models import (
    FretPassenger,  JourneyClientFolder, JourneySession, Passenger,
    PlaceReserved, SeletectedJourney,  OtherInfoReservation, ResearchReservation
)
# Register your models here.
admin.site.register(ResearchReservation)
admin.site.register(JourneyClientFolder)
admin.site.register(SeletectedJourney)
admin.site.register(FretPassenger)
admin.site.register(Passenger)
admin.site.register(JourneySession)
admin.site.register(PlaceReserved)
admin.site.register(OtherInfoReservation)
