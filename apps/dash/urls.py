from rest_framework.routers import DefaultRouter

from .views import (
    CarsView, SeatView, JourneyView, RoutingView, CoverCityView,
    PointOfSaleView, PointOfSaleWorkerView, CabinePlaneView
)

router = DefaultRouter()
router.register(r'technic/cars', CarsView, basename='cars')
router.register(r'technic/seat', SeatView, basename='seat')
router.register(r'technic/cabine_plane',
                CabinePlaneView, basename='cabine_plane')
router.register(r'transport/journey', JourneyView, basename='journey')
router.register(r'transport/routing', RoutingView, basename='routing')
router.register(r'transport/cover_city', CoverCityView, basename='cover_city')
router.register(r'transport/pos', PointOfSaleView, basename='point_of_sale')
router.register(r'transport/pos_worker', PointOfSaleWorkerView,
                basename='point_of_sale_worker')

urlpatterns = router.urls
