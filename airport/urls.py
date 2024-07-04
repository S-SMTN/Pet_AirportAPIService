from django.urls import path, include
from rest_framework import routers

from airport.views import (
    AirportViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet
)

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplanetype", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"