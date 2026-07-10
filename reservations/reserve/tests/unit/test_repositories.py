import pytest
from datetime import date
from reserve.repositories import LocationRepository, ReservationRepository
from reserve.models import Location, Reservation
from django.core.cache import cache

@pytest.fixture
def location(db):
    return Location.objects.create(name="Meeting room", address_line="45th street", 
                                   country="BR", capacity=10, is_available=True)

@pytest.fixture
def existing_reservation(db, location, regular_user):
    return Reservation.objects.create(location=location, reserved_by=regular_user, 
                                      start_date=date(2026, 8, 1), end_date=date(2026, 8, 5), 
                                      num_people=3)

@pytest.mark.django_db
def test_has_conflict_detects_overlap(existing_reservation, location):
    assert ReservationRepository.has_conflict(location.id, date(2026, 8, 3), 
                                              date(2026, 8, 7)) is True
    
@pytest.mark.django_db
def test_has_conflict_no_overlap(existing_reservation, location):
    assert ReservationRepository.has_conflict(location.id, date(2026, 8, 6), date(2026, 8, 10)
                                              ) is False
    
@pytest.mark.django_db
def test_has_conflict_excludes_own_reservation(existing_reservation, location):
    assert ReservationRepository.has_conflict(location.id, date(2026, 8, 1), date(2026, 8, 5),
                                              exclude_id=existing_reservation.reservation_id) is False
    
@pytest.mark.django_db
def test_location_respository_sets_cache(location):
    cache.clear()
    qs = LocationRepository.get_ordered()
    cached = cache.get(LocationRepository.CACHE_KEY)
    assert cache is not None
    assert list(qs) == list(cached)