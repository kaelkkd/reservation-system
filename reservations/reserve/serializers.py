from rest_framework import serializers
from .models import Location, Reservation
from .mixins import ReservationValidationMixin

class LocationSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source="address_line")
    class Meta:
        model = Location
        fields = (
            'id',
            'name',
            'address',
            'country',
            'capacity'
        )
    
    def validate(self, value):
        if value <= 0:
            raise serializers.ValidationError({"capacity": "The capacity must be at least 1."})
        return value
    
class ReservationSerializer(ReservationValidationMixin, serializers.ModelSerializer):
    reservation_id = serializers.UUIDField(read_only=True)
    reserved_at = serializers.CharField(source="created_at", read_only=True)
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), source="location", write_only=True)
    number_of_people = serializers.IntegerField(source="num_people")
    user = serializers.PrimaryKeyRelatedField(source="reserved_by", read_only=True)

    class Meta:
        model = Reservation
        fields = (
            'reservation_id',
            'user',
            'location',
            'location_id',
            'start_date',
            'end_date',
            'reserved_at',
            'number_of_people'
        )

    def create(self, validated_data):
        validated_data["reserved_by"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, attrs):
        location = attrs.get("location")
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        num_people = attrs.get("num_people")
        self.validate_dates(start, end)
        self.validate_capacity(num_people, location)
        if self.validate_overlap(location, start, end):
            raise serializers.ValidationError({"non_fiel_errors": "Location not available at the selected date."})
        
        return attrs      

class UpdateReservationSerializer(ReservationValidationMixin, serializers.ModelSerializer):
    reservation_id = serializers.UUIDField(read_only=True)
    reserved_at = serializers.CharField(source="created_at", read_only=True)
    location = LocationSerializer(read_only=False)
    location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), source="location", read_only=True)
    number_of_people = serializers.IntegerField(source="num_people")
    user = serializers.PrimaryKeyRelatedField(source="reserved_by", read_only=True)

    class Meta:
        model = Reservation
        fields = (
            'reservation_id',
            'user',
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
        self.validate_dates(start, end)
        self.validate_capacity(num_people, location)
        if self.validate_overlap(location, start, end, exclude_id=self.instance.reservation_id):
            raise serializers.ValidationError({"non_fiel_errors": "Location not available at the selected date."})
        
        return attrs