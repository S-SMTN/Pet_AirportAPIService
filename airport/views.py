from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.serializers import ModelSerializer
from django.db.models.query import QuerySet

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew
)
from airport.serializers import (
    AirportSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneRetrieveSerializer,
    CrewSerializer,
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
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteRetrieveSerializer

        return RouteSerializer

    def get_queryset(self) -> QuerySet:
        if self.action in ("list", "retrieve"):
            return Route.objects.all().select_related("source", "destination")
        return Route.objects.all()


class AirplaneTypeViewSet(ReadUpdateModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(ReadUpdateModelViewSet):
    queryset = Airplane.objects.all()

    def get_serializer_class(self) -> type[ModelSerializer]:
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneRetrieveSerializer
        return AirplaneSerializer

    def get_queryset(self) -> QuerySet:
        if self.action in ("list", "retrieve"):
            return Airplane.objects.all().select_related("airplane_type")
        return Airplane.objects.all()


class CrewViewSet(ReadUpdateModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
