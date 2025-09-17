from django.contrib import admin
from users.models import User
from reserve.models import Reservation, Location
# Register your models here.

admin.site.register(User)
admin.site.register(Reservation)
admin.site.register(Location)