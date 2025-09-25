from django.urls import path
from . import views
from rest_framework import routers

urlpatterns = [
    path('reserve/', views.ReservationListCreateAPIView.as_view()),
    path('reserve/info/<uuid:reservation_id>/', views.ReservationDetailAPIView.as_view()),
]

router = routers.DefaultRouter()
router.register('locations', views.LocationViewSet)
urlpatterns += router.urls