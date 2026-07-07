class ReservationError(Exception):
    pass

class ReservationConflictError(ReservationError):
    "The property is not available at the selected date."
    pass

class ReservationCapacityExcedeedError(ReservationError):
    "num_people exceeds the maximum capacity"
    pass

class InvalidDateRangeError(ReservationError):
    "end_date must be after start_date"
    pass