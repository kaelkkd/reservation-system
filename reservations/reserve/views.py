from rest_framework import viewsets
from .models import Location, Reservation
from .filters import LocationFilter
from .serializers import LocationSerializer, ReservationSerializer, ReservationUpdateSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .repositories import LocationRepository
from .services import ReservationService

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.order_by('pk')
    serializer_class = LocationSerializer
    filterset_class = LocationFilter

    def get_queryset(self):
        return LocationRepository.get_ordered()

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]

        return super().get_permissions()
    
class ReservationViewSet(viewsets.ModelViewSet):
    lookup_field = "reservation_id"
    lookup_url_kwarg = "reservation_id"
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return ReservationUpdateSerializer
        return ReservationSerializer
        
    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.all() if user.is_staff else Reservation.objects.filter(reserved_by=user)
    
    def perform_create(self, serializer):
        reservation = serializer.save(reserved_by=self.request.user)
        ReservationService.confirm_reservation(reservation)

    def perform_destroy(self, instance):
        ReservationService.confirm_cancellation(instance)
        instance.delete()
