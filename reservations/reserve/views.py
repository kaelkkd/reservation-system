from rest_framework import viewsets
from .models import Location, Reservation
from .filters import LocationFilter
from .serializers import LocationSerializer, ReservationSerializer, ReservationUpdateSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .tasks import send_reservation_confirmation, send_cancellation_confirmation

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.order_by('pk')
    serializer_class = LocationSerializer
    filterset_class = LocationFilter

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        qs = cache.get("locations_qs")
        if qs is None:
            qs = Location.objects.order_by("pk")
            cache.set("locations_qs", qs, 60 * 15)
        
        return qs

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
        send_reservation_confirmation.delay(reservation.reservation_id, self.request.user.email)

    def perform_destroy(self, instance):
        send_cancellation_confirmation(instance.reservation_id, instance.reserved_by.email)
        instance.delete()
