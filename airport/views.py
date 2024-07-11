from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.serializers import ModelSerializer
from django.db.models.query import QuerySet

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order
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
    FlightSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer,
    OrderSerializer,
    OrderListSerializer,
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


class FlightViewSet(ReadUpdateModelViewSet):
    queryset = Flight.objects.all()

    def get_serializer_class(self) -> type[ModelSerializer]:
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightRetrieveSerializer
        return FlightSerializer

    def get_queryset(self) -> QuerySet:
        if self.action in ("list", "retrieve"):
            return Flight.objects.all().select_related(
                "route__source",
                "route__destination",
                "airplane__airplane_type",
            ).prefetch_related(
                "crew",
            )
        return Flight.objects.all()


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.all()

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related(
                "tickets__flight__crew",
            ).select_related("user")

        return queryset

    def perform_create(self, serializer: ModelSerializer) -> None:
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer
