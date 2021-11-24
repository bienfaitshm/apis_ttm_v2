from django.contrib import admin
from .models import (
    FretPassenger,  JourneyClientFolder, JourneySession, Passenger,
    PlaceReserved, SeletectedJourney, ValidationPayment
)
# Register your models here.

admin.site.register(JourneyClientFolder)
admin.site.register(SeletectedJourney)
admin.site.register(FretPassenger)
admin.site.register(Passenger)
admin.site.register(ValidationPayment)
admin.site.register(JourneySession)
admin.site.register(PlaceReserved)