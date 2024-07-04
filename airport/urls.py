from django.urls import path, include
from rest_framework import routers

from airport.views import (
    AirportViewSet,
    RouteViewSet
)

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
