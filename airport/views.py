from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.serializers import ModelSerializer
from django.db.models.query import QuerySet

from airport.models import (
    Airport,
    Route
)
from airport.serializers import (
    AirportSerializer,
    RouteSerializer, RouteListSerializer
)


class ReadUpdateModelViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    pass


class AirportViewSet(ReadUpdateModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(ReadUpdateModelViewSet):
    queryset = Route.objects.all()

    def get_serializer_class(self) -> type[ModelSerializer]:
        if self.action in ("list", "retrieve"):
            return RouteListSerializer

        return RouteSerializer

    def get_queryset(self) -> QuerySet:
        if self.action == "list":
            return Route.objects.all().select_related("source", "destination")
        return Route.objects.all()
