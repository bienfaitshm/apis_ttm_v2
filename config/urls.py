from django.contrib import admin
from django.urls import path, re_path, include
from .views import current_datetime, index
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie
from django.conf.urls.static import static
from django.conf import settings
from .schemas import schema
from graphene_django.views import GraphQLView


schema_view = get_schema_view(
    openapi.Info(
        title="Ttm API",
        default_version='v1',
        description="documentation of api ttm",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@jungostudy.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("time", current_datetime),
    path("",index),
    # documentaion route...
    re_path(r'^docs/swagger(?P<format>\.json|\.yaml)/$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("docs/swagger/", schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path("docs/redoc/", schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    # authentication routing
    path("accounts/", include('djoser.urls')),
    path("accounts/", include('djoser.urls.authtoken')),
    path("accounts/", include('djoser.urls.jwt')),
    path("accounts/", include("apps.account.urls")),
    # main
    path("", include("apps.dash.urls")),
    path("", include("apps.clients.urls")),
    path('graphql/', csrf_exempt(
            jwt_cookie(
                GraphQLView.as_view(graphiql=True, schema=schema)))),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
