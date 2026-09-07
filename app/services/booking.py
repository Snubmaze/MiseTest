from datetime import date
from sqlalchemy.exc import IntegrityError
from app.exceptions import BookingNotFoundError, BookingSlotConflictError
from app.models.booking import Booking, BookingStatus
from app.repositories.booking import BookingRepository
from app.schemas.booking import BookingCreate


class BookingService:
    def __init__(self, repository: BookingRepository) -> None:
        self._repository = repository

    async def create_booking(self, booking_data: BookingCreate) -> Booking:
        occupied_booking = await self._repository.get_active_by_slot(
            booking_data.booking_date,
            booking_data.booking_time,
        )
        if occupied_booking is not None:
            raise BookingSlotConflictError()

        booking = Booking(**booking_data.model_dump())
        try:
            return await self._repository.create(booking)
        except IntegrityError as error:
            raise BookingSlotConflictError() from error

    async def list_bookings(
        self,
        booking_date: date | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Booking]:
        return await self._repository.list(booking_date, offset, limit)

    async def get_booking(self, booking_id: int) -> Booking:
        booking = await self._repository.get_by_id(booking_id)
        if booking is None:
            raise BookingNotFoundError()
        return booking

    async def cancel_booking(self, booking_id: int) -> Booking:
        booking = await self.get_booking(booking_id)
        if booking.status == BookingStatus.CANCELLED:
            return booking
        booking.status = BookingStatus.CANCELLED
        return await self._repository.save(booking)
