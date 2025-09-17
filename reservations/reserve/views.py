from django.shortcuts import render
from rest_framework import generics
from .models import Location, Reservation
from .serializers import LocationSerializer, ReservationSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
# Create your views here.

class LocationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()
    
class LocationDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_url_kwarg = "location_id"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
class ReservationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reservation.objects.prefetch_related("location")
    serializer_class = ReservationSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(reserved_by=self.request.user)
    
class ReservationDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = ReservationSerializer
    lookup_url_kwarg = "reservation_id"

    def get_queryset(self):
        user = self.request.user
        return Reservation.object.all() if user.is_staff else Reservation.objects.filter(reserved_by=user)