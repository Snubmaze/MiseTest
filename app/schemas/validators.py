from datetime import date, time, timedelta


def validate_name(value: str) -> str:
    if not any(character.isalpha() for character in value):
        raise ValueError("Name must contain letters")
    if not all(character.isalpha() or character in " -" for character in value):
        raise ValueError("Name may contain only letters, spaces, and hyphens")
    return value


def validate_booking_time(value: time) -> time:
    if value.tzinfo is not None:
        raise ValueError("Booking time must not include a timezone")
    if value.minute != 0 or value.second != 0 or value.microsecond != 0:
        raise ValueError("Booking time must be a full-hour slot")
    if not 12 <= value.hour <= 22:
        raise ValueError("Booking time must be between 12:00 and 22:00")
    return value


def validate_booking_date(value: date) -> date:
    today = date.today()
    if not today <= value <= today + timedelta(days=90):
        raise ValueError("Booking date must be between today and 90 days from today")
    return value
