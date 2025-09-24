from rest_framework import generics, filters, viewsets
from .models import Location, Reservation
from .filters import LocationFilter
from .serializers import LocationSerializer, ReservationSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.order_by('pk')
    serializer_class = LocationSerializer
    filterset_class = LocationFilter
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()
    
class ReservationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Reservation.objects.select_related("location")
        return queryset if user.is_staff else queryset.filter(reserved_by=user)
            
    def perform_create(self, serializer):
        serializer.save(reserved_by=self.request.user)
    
class ReservationDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = ReservationSerializer
    lookup_field = "reservation_id"
    lookup_url_kwarg = "reservation_id"

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.all() if user.is_staff else Reservation.objects.filter(reserved_by=user)