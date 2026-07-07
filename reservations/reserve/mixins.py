from rest_framework import serializers
from .repositories import ReservationRepository

class ReservationValidationMixin:
    def validate_dates(self, start_date, end_date):
        if start_date >= end_date:
            raise serializers.ValidationError({"date": "End date must be after start date."})
        
    def validate_capacity(self, num_people, location):
        if num_people > location.capacity:
            raise serializers.ValidationError({"number_of_people": "The location cannot accommodate that many people."})

    def validate_overlap(self, location, start_date, end_date, exclude_id=None):
        if ReservationRepository.has_conflict(location.id, start_date, end_date, exclude_id):
            raise serializers.ValidationError({"non_field_errors": "Location not available at the selected date."})

