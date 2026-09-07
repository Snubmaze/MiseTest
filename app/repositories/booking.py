from datetime import date, time
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.booking import Booking, BookingStatus


class BookingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, booking: Booking) -> Booking:
        self._session.add(booking)
        return await self._commit(booking)

    async def _commit(self, booking: Booking) -> Booking:
        try:
            await self._session.commit()
        except SQLAlchemyError:
            await self._session.rollback()
            raise
        await self._session.refresh(booking)
        return booking

    async def list(
        self,
        booking_date: date | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Booking]:
        statement = select(Booking)
        if booking_date is not None:
            statement = statement.where(Booking.booking_date == booking_date)
        statement = statement.order_by(
            Booking.booking_date,
            Booking.booking_time,
            Booking.id,
        ).offset(offset).limit(limit)
        result = await self._session.scalars(statement)
        return list(result.all())

    async def get_by_id(self, booking_id: int) -> Booking | None:
        return await self._session.get(Booking, booking_id)

    async def get_active_by_slot(
        self,
        booking_date: date,
        booking_time: time,
    ) -> Booking | None:
        statement = select(Booking).where(
            Booking.booking_date == booking_date,
            Booking.booking_time == booking_time,
            Booking.status == BookingStatus.ACTIVE,
        )
        return await self._session.scalar(statement)

    async def save(self, booking: Booking) -> Booking:
        return await self._commit(booking)
