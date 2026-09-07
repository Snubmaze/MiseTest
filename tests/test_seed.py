from datetime import date
import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.models.booking import Booking
from app.seed import build_demo_bookings, seed_bookings


def test_demo_bookings_use_relative_dates() -> None:
    today = date(2026, 9, 7)

    bookings = build_demo_bookings(today)

    offsets = [
        booking.booking_date.toordinal() - today.toordinal()
        for booking in bookings
    ]

    assert offsets == [1, 2, 7]


@pytest.mark.asyncio
async def test_seed_is_idempotent(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    bookings = build_demo_bookings(date.today())

    assert await seed_bookings(session_factory, bookings) == 3
    assert await seed_bookings(session_factory, bookings) == 0

    async with session_factory() as session:
        count = await session.scalar(select(func.count()).select_from(Booking))

    assert count == 3
