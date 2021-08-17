from rest_framework.routers import DefaultRouter

from .views import ClientView, CompanyView, EmployeView

router = DefaultRouter()
router.register(r'clients', ClientView, basename='clients')
router.register(r'company', CompanyView, basename='company')
router.register(r'employe', EmployeView, basename='employe')

urlpatterns = router.urls
