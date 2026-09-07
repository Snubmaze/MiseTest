from datetime import date, time
from typing import Annotated
from pydantic import AfterValidator, BaseModel, ConfigDict, Field
from app.models.booking import BookingStatus
from app.schemas.validators import validate_booking_date, validate_booking_time, validate_name


Name = Annotated[
    str,
    Field(min_length=2, max_length=100, examples=["Анна Смирнова"]),
    AfterValidator(validate_name),
]
Phone = Annotated[
    str,
    Field(pattern=r"^(?:\+7|8)\d{10}$", examples=["+79991234567"]),
]
BookingDate = Annotated[date, AfterValidator(validate_booking_date)]
BookingTime = Annotated[time, AfterValidator(validate_booking_time)]
Guests = Annotated[int, Field(strict=True, ge=1, le=12, examples=[4])]


class BookingBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Name
    phone: Phone
    booking_date: date = Field(examples=["2026-09-20"])
    booking_time: BookingTime = Field(examples=["19:00"])
    guests: Guests


class BookingCreate(BookingBase):
    booking_date: BookingDate = Field(examples=["2026-09-20"])


class BookingOut(BookingBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int = Field(gt=0, examples=[1])
    status: BookingStatus
