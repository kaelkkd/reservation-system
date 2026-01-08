from . import views
from rest_framework import routers

urlpatterns = [

]

router = routers.DefaultRouter()
router.register('locations', views.LocationViewSet)
router.register('reserve', views.ReservationViewSet, basename="reservation")
urlpatterns += router.urls