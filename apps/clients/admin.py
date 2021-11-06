from django.contrib import admin
from .models import (
    FretPassenger, Journey, JourneyClientFolder, JourneySession, Passenger,
    PlaceReserved, Routing, Seat, SeletectedJourney
)
# Register your models here.

admin.site.register(FretPassenger)
admin.site.register(Journey)
admin.site.register(JourneyClientFolder)
admin.site.register(JourneySession)
admin.site.register(PlaceReserved)
admin.site.register(Routing)
admin.site.register(Seat)
admin.site.register(SeletectedJourney)