from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query, status
from app.api.dependencies import get_booking_service
from app.schemas.booking import BookingCreate, BookingOut
from app.services.booking import BookingService


router = APIRouter(prefix="/bookings", tags=["bookings"])
BookingServiceDependency = Annotated[BookingService, Depends(get_booking_service)]


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    service: BookingServiceDependency,
) -> BookingOut:
    booking = await service.create_booking(booking_data)
    return BookingOut.model_validate(booking)


@router.get("", response_model=list[BookingOut])
async def list_bookings(
    service: BookingServiceDependency,
    booking_date: Annotated[date | None, Query(alias="date")] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[BookingOut]:
    bookings = await service.list_bookings(booking_date, offset, limit)
    return [BookingOut.model_validate(booking) for booking in bookings]


@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking(
    booking_id: Annotated[int, Path(gt=0)],
    service: BookingServiceDependency,
) -> BookingOut:
    booking = await service.get_booking(booking_id)
    return BookingOut.model_validate(booking)


@router.delete("/{booking_id}", response_model=BookingOut)
async def cancel_booking(
    booking_id: Annotated[int, Path(gt=0)],
    service: BookingServiceDependency,
) -> BookingOut:
    booking = await service.cancel_booking(booking_id)
    return BookingOut.model_validate(booking)
