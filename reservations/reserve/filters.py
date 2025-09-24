import django_filters
from reserve.models import Location, Reservation

class LocationFilter(django_filters.FilterSet):
    class Meta:
        model = Location
        fields = {
            'name': ['iexact', 'icontains'],
            'capacity': ['exact', 'lt', 'gt']
        }