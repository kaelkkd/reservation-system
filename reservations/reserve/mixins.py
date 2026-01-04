from rest_framework import serializers
from .models import Reservation

class ReservationValidationMixin:
    def validate_dates(self, start_date, end_date):
        if start_date >= end_date:
            raise serializers.ValidationError({"date": "End date must be after start date."})
        
    def validate_capacity(self, num_people, location):
        if num_people > location.capacity:
            raise serializers.ValidationError({"number_of_people": "The location cannot acommodate that many people."})

    def validate_overlap(self, location, start_date, end_date, exclude_id=None):
        query = Reservation.objects.filter(location=location, start_date__lt=end_date, end_date__gt=start_date)
        if exclude_id:
            query = query.exclude(reservation_id=exclude_id)
        
        return query.exists()
