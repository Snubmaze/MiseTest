from datetime import date, timedelta
import pytest
from pydantic import ValidationError
from app.schemas.booking import BookingCreate
from tests.factories import booking_payload


@pytest.mark.parametrize(
    "payload",
    [
        booking_payload(
            name="Ан",
            booking_date=date.today(),
            booking_time="12:00",
            guests=1,
        ),
        booking_payload(
            name="Anne-Marie",
            phone="89991234567",
            booking_date=date.today() + timedelta(days=90),
            booking_time="22:00",
            guests=12,
        ),
    ],
)
def test_booking_schema_accepts_boundary_values(payload: dict[str, object]) -> None:
    booking = BookingCreate.model_validate(payload)

    assert booking.name == payload["name"]


@pytest.mark.parametrize(
    "payload",
    [
        booking_payload(name="A"),
        booking_payload(name="Анна1"),
        booking_payload(name="--"),
        booking_payload(phone="+7 9991234567"),
        booking_payload(phone="79991234567"),
        booking_payload(booking_date=date.today() - timedelta(days=1)),
        booking_payload(booking_date=date.today() + timedelta(days=91)),
        booking_payload(booking_time="11:00"),
        booking_payload(booking_time="22:01"),
        booking_payload(booking_time="12:00:01"),
        booking_payload(guests=0),
        booking_payload(guests=13),
        {**booking_payload(), "guests": 4.5},
    ],
)
def test_booking_schema_rejects_invalid_values(payload: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        BookingCreate.model_validate(payload)
