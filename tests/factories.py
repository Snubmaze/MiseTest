from datetime import date, time, timedelta
from app.schemas.booking import BookingCreate


def booking_payload(
    *,
    name: str = "Анна Смирнова",
    phone: str = "+79991234567",
    booking_date: date | None = None,
    booking_time: str = "18:00",
    guests: int = 4,
) -> dict[str, object]:
    selected_date = booking_date or date.today() + timedelta(days=1)
    return {
        "name": name,
        "phone": phone,
        "booking_date": selected_date.isoformat(),
        "booking_time": booking_time,
        "guests": guests,
    }


def booking_create(
    *,
    name: str = "Анна Смирнова",
    booking_date: date | None = None,
    booking_time: time = time(18, 0),
) -> BookingCreate:
    selected_date = booking_date or date.today() + timedelta(days=1)
    return BookingCreate(
        name=name,
        phone="+79991234567",
        booking_date=selected_date,
        booking_time=booking_time,
        guests=4,
    )
