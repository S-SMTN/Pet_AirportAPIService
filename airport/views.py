from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import GenericViewSet

from airport.models import Airport
from airport.serializers import AirportSerializer


class AirportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    #permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
