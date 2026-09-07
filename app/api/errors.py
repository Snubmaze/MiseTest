from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.exceptions import BookingNotFoundError, BookingSlotConflictError


async def booking_not_found_handler(
    _request: Request,
    error: BookingNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(error)},
    )


async def booking_slot_conflict_handler(
    _request: Request,
    error: BookingSlotConflictError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(error)},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BookingNotFoundError, booking_not_found_handler)
    app.add_exception_handler(BookingSlotConflictError, booking_slot_conflict_handler)
