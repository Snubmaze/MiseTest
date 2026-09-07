from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.repositories.booking import BookingRepository
from app.services.booking import BookingService


SessionDependency = Annotated[AsyncSession, Depends(get_session)]


def get_booking_service(session: SessionDependency) -> BookingService:
    return BookingService(BookingRepository(session))
