class BookingError(Exception):
    pass


class BookingNotFoundError(BookingError):
    def __init__(self) -> None:
        super().__init__("Booking not found")


class BookingSlotConflictError(BookingError):
    def __init__(self) -> None:
        super().__init__("Booking slot is already occupied")
