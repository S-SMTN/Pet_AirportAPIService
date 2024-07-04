from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import Airport, Route, AirplaneType


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

    def validate(self, attrs: dict):
        data = super(RouteSerializer, self).validate(attrs=attrs)
        if attrs["source"] == attrs["destination"]:
            Route.validate_route(
                source=attrs["source"],
                destination=attrs["destination"],
                error_to_raise=ValidationError
            )
        return data


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )
    destination = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")
