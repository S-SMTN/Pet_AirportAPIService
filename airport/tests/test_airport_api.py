from datetime import datetime

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket,
)
from airport.serializers import OrderListSerializer
from user.models import User

ORDER_URL = reverse("airport:order-list")


class Database:
    def __init__(self, user: User) -> None:
        self.airport_1 = Airport.objects.create(
            name="Heathrow",
            closest_big_city="London"
        )
        self.airport_2 = Airport.objects.create(
            name="LaGuardia",
            closest_big_city="New York"
        )
        self.route = Route.objects.create(
            source=self.airport_1,
            destination=self.airport_2,
            distance=5552
        )
        self.airplanetype = AirplaneType.objects.create(
            name="Widebody"
        )
        self.airplane = Airplane.objects.create(
            name="Boeing 777",
            rows=18,
            seats_in_row=10,
            airplane_type=self.airplanetype
        )
        self.crew_member = Crew.objects.create(
            first_name="David",
            last_name="Linch"
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=datetime(2024, 1, 10, hour=11, minute=30),
            arrival_time=datetime(2024, 1, 10, hour=15, minute=30)
        )
        self.user = user
        self.order = Order.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            row=1,
            seat=1,
            flight=self.flight,
            order=self.order
        )


class UnauthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self) -> None:
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test",
            "testpass",
        )
        self.client.force_authenticate(self.user)
        self.data = Database(self.user)
        self.user2 = get_user_model().objects.create_user(
            "test2",
            "testpass2",
        )
        self.order2 = Order.objects.create(user=self.user2)
        self.ticket2 = Ticket.objects.create(
            row=2,
            seat=2,
            flight=self.data.flight,
            order=self.data.order
        )

    def test_list_orders(self) -> None:
        res = self.client.get(ORDER_URL)

        serializer = OrderListSerializer((self.data.order,), many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)
