import uuid
from django.db import models
from users.models import User, CountryChoices
from django.core.validators import MaxValueValidator

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=200, blank=False)
    address_line = models.CharField(max_length=250, blank=False)
    country = models.CharField(choices=CountryChoices.choices, blank=False)
    capacity = models.IntegerField(validators=[MaxValueValidator(15)], blank=False)
    is_available = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return f"{self.name} at {self.address_line} with a capacity of {self.capacity}"
    
class Reservation(models.Model):
    reservation_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="location")
    reserved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    num_people = models.IntegerField(validators=[MaxValueValidator(15)], blank=False)

    def __str__(self):
        return f"{self.location} reserved from {self.start_date} to {self.end_date}."


