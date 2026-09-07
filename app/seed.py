from asyncio import run
from collections.abc import Sequence
from datetime import date, time, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.core.config import get_settings
from app.core.database import engine, session_factory
from app.exceptions import BookingSlotConflictError
from app.repositories.booking import BookingRepository
from app.schemas.booking import BookingCreate
from app.services.booking import BookingService


def build_demo_bookings(today: date | None = None) -> tuple[BookingCreate, ...]:
    base_date = today or date.today()
    return (
        BookingCreate(
            name="Анна Смирнова",
            phone="+79991234567",
            booking_date=base_date + timedelta(days=1),
            booking_time=time(18),
            guests=2,
        ),
        BookingCreate(
            name="Иван Петров",
            phone="89991234568",
            booking_date=base_date + timedelta(days=2),
            booking_time=time(19),
            guests=4,
        ),
        BookingCreate(
            name="Мария Волкова",
            phone="+79991234569",
            booking_date=base_date + timedelta(days=7),
            booking_time=time(20),
            guests=6,
        ),
    )


async def seed_bookings(
    factory: async_sessionmaker[AsyncSession] = session_factory,
    bookings: Sequence[BookingCreate] | None = None,
) -> int:
    created = 0
    seed_items = bookings if bookings is not None else build_demo_bookings()
    async with factory() as session:
        service = BookingService(BookingRepository(session))
        for booking in seed_items:
            try:
                await service.create_booking(booking)
            except BookingSlotConflictError:
                continue
            created += 1
    return created


async def main() -> None:
    if get_settings().seed_demo_data:
        await seed_bookings()
    await engine.dispose()


if __name__ == "__main__":
    run(main())
