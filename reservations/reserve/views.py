from rest_framework import generics, filters, viewsets
from .models import Location, Reservation
from .filters import LocationFilter
from .serializers import LocationSerializer, ReservationSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .tasks import send_reservation_confirmation

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.order_by('pk')
    serializer_class = LocationSerializer
    filterset_class = LocationFilter
    filter_backends = [DjangoFilterBackend]

    @method_decorator(cache_page(60 * 15, key_prefix='location_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]

        return super().get_permissions()
    
class ReservationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Reservation.objects.select_related("location")
        return queryset if user.is_staff else queryset.filter(reserved_by=user)
            
    def perform_create(self, serializer):
        reservation = serializer.save(reserved_by=self.request.user)
        send_reservation_confirmation.delay(reservation.reservation_id, self.request.user.email)
    
class ReservationDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = ReservationSerializer
    lookup_field = "reservation_id"
    lookup_url_kwarg = "reservation_id"

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.all() if user.is_staff else Reservation.objects.filter(reserved_by=user)