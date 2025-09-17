from django.urls import path
from . import views

urlpatterns = [
    path('location/', views.LocationListCreateAPIView.as_view()),
    path('location/info/', views.LocationDetailAPIView.as_view()),
    path('reserve/', views.ReservationListCreateAPIView.as_view()),
    path('reserve/info/', views.ReservationDetailAPIView.as_view()),
]