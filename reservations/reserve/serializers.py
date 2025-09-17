from rest_framework import serializers
from .models import Location, Reservation

class LocationSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source="address_line")
    class Meta:
        model = Location
        fields = (
            'name',
            'address',
            'country',
            'capacity'
        )
    
    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Capacity must be greater than 0.")
        return value
    
class ReservationSerializer(serializers.ModelSerializer):
    reservation_id = serializers.UUIDField(read_only=True)
    reserved_at = serializers.CharField(source="created_at", read_only=True)
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), source="location", write_only=True)

    class Meta:
        model = Reservation
        fields = (
            'reservation_id',
            'location',
            'location_id',
            'start_date',
            'end_date',
            'reserved_at'
        )




    