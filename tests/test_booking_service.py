from datetime import date, time, timedelta
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import BookingNotFoundError, BookingSlotConflictError
from app.models.booking import Booking, BookingStatus
from app.repositories.booking import BookingRepository
from app.services.booking import BookingService
from tests.factories import booking_create


class StaleSlotRepository(BookingRepository):
    async def get_active_by_slot(
        self,
        booking_date: date,
        booking_time: time,
    ) -> Booking | None:
        return None


@pytest.mark.asyncio
async def test_create_list_filter_paginate_and_get_booking(
    booking_service: BookingService,
) -> None:
    first = await booking_service.create_booking(booking_create(booking_time=time(18, 0)))
    second = await booking_service.create_booking(booking_create(booking_time=time(19, 0)))
    third = await booking_service.create_booking(
        booking_create(
            booking_date=first.booking_date + timedelta(days=1),
            booking_time=time(18, 0),
        )
    )

    bookings = await booking_service.list_bookings()
    filtered = await booking_service.list_bookings(first.booking_date)
    paginated = await booking_service.list_bookings(offset=1, limit=1)
    fetched = await booking_service.get_booking(first.id)

    assert [booking.id for booking in bookings] == [first.id, second.id, third.id]
    assert [booking.id for booking in filtered] == [first.id, second.id]
    assert [booking.id for booking in paginated] == [second.id]
    assert fetched.id == first.id
    assert fetched.status == BookingStatus.ACTIVE


@pytest.mark.asyncio
async def test_missing_booking_has_exact_message(
    booking_service: BookingService,
) -> None:
    with pytest.raises(BookingNotFoundError, match="^Booking not found$"):
        await booking_service.get_booking(999_999)


@pytest.mark.asyncio
async def test_active_slot_conflict(
    booking_service: BookingService,
) -> None:
    data = booking_create()
    await booking_service.create_booking(data)

    with pytest.raises(BookingSlotConflictError):
        await booking_service.create_booking(data)


@pytest.mark.asyncio
async def test_integrity_error_is_mapped_to_slot_conflict(
    booking_service: BookingService,
    session: AsyncSession,
) -> None:
    data = booking_create()
    await booking_service.create_booking(data)
    stale_service = BookingService(StaleSlotRepository(session))

    with pytest.raises(BookingSlotConflictError):
        await stale_service.create_booking(data)


@pytest.mark.asyncio
async def test_cancellation_is_idempotent_and_releases_slot(
    booking_service: BookingService,
) -> None:
    data = booking_create()
    created = await booking_service.create_booking(data)

    cancelled = await booking_service.cancel_booking(created.id)
    cancelled_again = await booking_service.cancel_booking(created.id)
    replacement = await booking_service.create_booking(data)
    bookings = await booking_service.list_bookings()

    assert cancelled.status == BookingStatus.CANCELLED
    assert cancelled_again.id == created.id
    assert cancelled_again.status == BookingStatus.CANCELLED
    assert replacement.id != created.id
    assert replacement.status == BookingStatus.ACTIVE
    assert [booking.status for booking in bookings] == [
        BookingStatus.CANCELLED,
        BookingStatus.ACTIVE,
    ]
