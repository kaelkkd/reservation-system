from .models import Location, Reservation
from django.core.cache import cache

class LocationRepository:
    CACHE_KEY = "location_qs"
    CACHE_TTL = 60 * 15

    @staticmethod
    def get_ordered():
        qs = cache.get(LocationRepository.CACHE_KEY)
        if qs is None:
            qs = Location.objects.order_by("pk")
            cache.set(LocationRepository.CACHE_KEY, qs, LocationRepository.CACHE_TTL)

        return qs


class ReservationRepository:
    @staticmethod
    def has_conflict(location_id, start_date, end_date, exclude_id=None):
        qs = Reservation.objects.filter(
            location_id=location_id,
            start_date__lt=end_date,
            end_date__gt=start_date,
        )
        if exclude_id:
            qs = qs.exclude(reservation_id=exclude_id)

        return qs.exists()