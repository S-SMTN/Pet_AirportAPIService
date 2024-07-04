from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator

from AirportAPIService import settings


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Route(models.Model):
    source = models.ForeignKey(
        to=Airport,
        on_delete=models.PROTECT,
        related_name="routes_as_source"
    )
    destination = models.ForeignKey(
        to=Airport,
        on_delete=models.PROTECT,
        related_name="routes_as_destination"
    )
    distance = models.PositiveIntegerField()

    @property
    def full_route(self) -> str:
        return str(self)

    @staticmethod
    def validate_route(
            source: str,
            destination: str,
            error_to_raise: type[Exception]
    ) -> None:
        error_text = {
            "Route": "Source and destination must be different"
        }
        if source == destination:
            raise error_to_raise(error_text)

    def clean(self):
        self.validate_route(
            source=str(self.source),
            destination=str(self.destination),
            error_to_raise=ValidationError
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Route, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self) -> str:
        return f"{self.source}-{self.destination}"

    class Meta:
        ordering = ["source", "destination"]
        unique_together = ("source", "destination")


class AirplaneType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Airplane(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rows = models.PositiveIntegerField(
        default=1,
        validators=[MaxValueValidator(99)]
    )
    seats_in_row = models.PositiveIntegerField(
        default=1,
        validators=[MaxValueValidator(99)]
    )
    airplane_type = models.ForeignKey(
        to=AirplaneType,
        on_delete=models.PROTECT,
        related_name="airplanes"
    )

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Crew(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    @property
    def full_name(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["last_name"]


class Flight(models.Model):
    route = models.ForeignKey(
        to=Route,
        on_delete=models.PROTECT,
        related_name="flights"
    )
    airplane = models.ForeignKey(
        to=Airplane,
        on_delete=models.PROTECT,
        related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(
        to=Crew,
        related_name="flights"
    )

    def __str__(self) -> str:
        return f"{self.route} {self.departure_time}"

    class Meta:
        ordering = ["-departure_time"]


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    def __str__(self) -> str:
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(
        to=Flight,
        on_delete=models.PROTECT,
        related_name="tickets"
    )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.PROTECT,
        related_name="tickets"
    )

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {airplane_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight.airplane,
            ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self) -> str:
        return f"{self.flight} (row: {self.row}, seat: {self.seat})"

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["flight", "row", "seat"]
