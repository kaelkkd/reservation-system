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
    
    def validate(self, value):
        if value <= 0:
            raise serializers.ValidationError({"capacity": "The capacity must be at least 1."})
        return value
    
class ReservationSerializer(serializers.ModelSerializer):
    reservation_id = serializers.UUIDField(read_only=True)
    reserved_at = serializers.CharField(source="created_at", read_only=True)
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), source="location", write_only=True)
    number_of_people = serializers.IntegerField(source="num_people")

    class Meta:
        model = Reservation
        fields = (
            'reservation_id',
            'location',
            'location_id',
            'start_date',
            'end_date',
            'reserved_at',
            'number_of_people'
        )

    def validate(self, attrs):
        location = attrs.get("location")
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        num_people = attrs.get("num_people")

        if start >= end:
            raise serializers.ValidationError({"end_date": "End date must be after start date."})  
        
        overlaps = Reservation.objects.filter(location=location, start_date__lt=end, end_date__gt=start,).exists()
        if overlaps > 0:
            raise serializers.ValidationError({"non_fiel_errors": "Location not available at the selected date."})
        
        if num_people > location.capacity:
            raise serializers.ValidationError({"number_of_people": "The location cannot acommodate that many people."})
        
        return attrs      




    