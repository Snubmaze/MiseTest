from datetime import date, time
from enum import StrEnum
from sqlalchemy import CheckConstraint, Date, Enum, Index, SmallInteger, String, Time, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CheckConstraint, Date, Enum, Index, SmallInteger, String, Time, text
from app.core.database import Base


class BookingStatus(StrEnum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


booking_status_type = Enum(
    BookingStatus,
    name="booking_status",
    native_enum=False,
    create_constraint=True,
    values_callable=lambda statuses: [status.value for status in statuses],
)


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("guests BETWEEN 1 AND 12", name="guests_range"),
        Index("ix_bookings_booking_date", "booking_date"),
        Index(
            "uq_bookings_active_slot",
            "booking_date",
            "booking_time",
            unique=True,
            sqlite_where=text("status = 'active'"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(12))
    booking_date: Mapped[date] = mapped_column(Date)
    booking_time: Mapped[time] = mapped_column(Time)
    guests: Mapped[int] = mapped_column(SmallInteger)
    status: Mapped[BookingStatus] = mapped_column(
        booking_status_type,
        default=BookingStatus.ACTIVE,
        server_default=BookingStatus.ACTIVE.value,
    )
