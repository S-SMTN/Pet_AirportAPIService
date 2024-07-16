from datetime import datetime
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
from django.test import TestCase

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket
)


class ModelTests(TestCase):
    def setUp(self) -> None:
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
        self.user = get_user_model().objects.create_user(
            username="username",
            email="email@mail.com",
            password="test1234",
            last_name="last_name",
            first_name="last_name"
        )
        self.order = Order.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            row=1,
            seat=1,
            flight=self.flight,
            order=self.order
        )

    def test_airport_str(self) -> None:
        self.assertEqual(
            str(self.airport_1),
            f"{self.airport_1.name}"
        )

    def same_airport(self) -> None:
        Airport.objects.create(
            name=self.airport_1.name,
            closest_big_city=self.airport_1.closest_big_city
        )

    def test_airport_ununique(self) -> None:
        with self.assertRaises(expected_exception=IntegrityError):
            self.same_airport()

    def test_route_str(self) -> None:
        self.assertEqual(
            str(self.route),
            f"{self.route.source}-{self.route.destination}"
        )

    def same_route(self) -> None:
        Route.objects.create(
            source=self.airport_1,
            destination=self.airport_2,
            distance=5552
        )

    def test_route_unique(self) -> None:
        with self.assertRaises(expected_exception=ValidationError):
            self.same_route()

    def route_source_equals_destination(self) -> None:
        Route.objects.create(
            source=self.airport_2,
            destination=self.airport_2,
            distance=5552
        )

    def test_route_source_equals_destination(self) -> None:
        with self.assertRaises(expected_exception=ValidationError):
            self.route_source_equals_destination()

    def test_airplaine_type_str(self) -> None:
        self.assertEqual(
            str(self.airplanetype),
            f"{self.airplanetype.name}"
        )

    def same_airplane_type(self) -> None:
        AirplaneType.objects.create(
            name=self.airplanetype.name
        )

    def test_airplane_type_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            self.same_airplane_type()

    def test_airplaine_str(self) -> None:
        self.assertEqual(
            str(self.airplane),
            f"{self.airplane.name}"
        )

    def same_airplane(self) -> None:
        Airplane.objects.create(
            name=self.airplane.name
        )

    def test_airplane_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            self.same_airplane()

    def test_crew_str(self) -> None:
        self.assertEqual(
            str(self.crew_member),
            f"{self.crew_member.first_name} {self.crew_member.last_name}"
        )

    def test_flight_str(self) -> None:
        self.assertEqual(
            str(self.flight),
            f"{self.flight.route} {self.flight.departure_time}"
        )

    def test_order_str(self) -> None:
        self.assertEqual(
            str(self.order),
            f"{self.order.created_at}"
        )

    def test_ticket_str(self) -> None:
        self.assertEqual(
            first=str(self.ticket),
            second=(
                f"{self.ticket.flight} "
                f"(row: {self.ticket.row}, seat: {self.ticket.seat})"
            )
        )

    def same_ticket(self) -> None:
        Ticket.objects.create(
            row=self.ticket.row,
            seat=self.ticket.seat,
            flight=self.ticket.flight,
            order=self.ticket.order
        )

    def test_ticket_unique(self) -> None:
        with self.assertRaises(ValidationError):
            self.same_ticket()

    def test_incorrect_ticket_seat(self) -> None:
        with self.assertRaises(ValidationError):
            Ticket.objects.create(
                row=self.airplane.rows,
                seat=self.airplane.seats_in_row + 1,
                flight=self.ticket.flight,
                order=self.ticket.order
            )

    def test_incorrect_ticket_row(self) -> None:
        with self.assertRaises(ValidationError):
            Ticket.objects.create(
                row=self.airplane.rows + 1,
                seat=self.airplane.seats_in_row,
                flight=self.ticket.flight,
                order=self.ticket.order
            )
