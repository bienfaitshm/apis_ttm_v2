from django.contrib import admin
from .models import (
    CabinePlane, Cars, CoverCity,  Journey, PointOfSale,
    PointOfSaleWorker,RouteJourney, Routing, Seat
)


admin.site.register(CoverCity)

admin.site.register(Journey)

admin.site.register(Cars)
admin.site.register(CabinePlane)
admin.site.register(Seat)
admin.site.register(PointOfSale)
admin.site.register(PointOfSaleWorker)
admin.site.register(RouteJourney)
admin.site.register(Routing)