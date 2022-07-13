from django.contrib import admin
from .models import (
    CabinePlane, Cars, CoverCity,  Journey, PointOfSale,
    PointOfSaleWorker, Routing, Seat, JourneyClass, JourneyTarif, Ticket
)


admin.site.register(CoverCity)

admin.site.register(Journey)

admin.site.register(Cars)
admin.site.register(CabinePlane)
admin.site.register(Seat)
admin.site.register(PointOfSale)
admin.site.register(PointOfSaleWorker)
admin.site.register(JourneyClass)
admin.site.register(JourneyTarif)
admin.site.register(Routing)
admin.site.register(Ticket)
