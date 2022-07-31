from django.contrib import admin

from .models import (
    FretPassenger, JourneyClientFolder, JourneySession, OtherInfoReservation,
    Passenger, PlaceReserved, ResearchReservation, SeletectedJourney,
)

# Register your models here.
admin.site.register(ResearchReservation)
admin.site.register(JourneyClientFolder)
admin.site.register(FretPassenger)
admin.site.register(JourneySession)
admin.site.register(PlaceReserved)
admin.site.register(OtherInfoReservation)


@admin.register(SeletectedJourney)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'pnr', 'status')


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'journey')
