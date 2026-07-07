from .repositories import ReservationRepository
from .tasks import send_reservation_confirmation, send_cancellation_confirmation
from .exceptions import ReservationCapacityExcedeedError, ReservationConflictError, InvalidDateRangeError

class ReservationService:
    @staticmethod
    def validate_and_create(reservation, location):
        if reservation.end_date <= reservation.start_date:
            raise InvalidDateRangeError("end_date must be after start_date")
        
        if reservation.num_people > location.capacity:
            raise ReservationCapacityExcedeedError(f"num_people ({reservation.num_people}) exceeds location_capacity ({location.capacity})")
        
        if ReservationRepository.has_conflict(location.id, reservation.start_date, reservation.end_date):
            raise ReservationConflictError("A reservation already exists for this location in the given period.")
        
    @staticmethod
    def confirm_reservation(reservation):
        send_reservation_confirmation.delay(str(reservation.reservation_id),
                                            reservation.reserved_by.email)
        
    @staticmethod
    def confirm_cancellation(reservation):
        send_cancellation_confirmation.delay(str(reservation.reservation_id),
                                             reservation.reserved_by.email)