from fastapi import FastAPI
from app.api.bookings import router as bookings_router
from app.api.errors import register_exception_handlers
from app.core.config import get_settings


settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(bookings_router)
register_exception_handlers(app)
