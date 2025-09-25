from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from reserve.models import Location
from django.core.cache import cache

@receiver([post_save, post_delete], sender=Location)
def invalidate_location_cache(sender, instance, **kwargs):
    print("Clearing location cache")
    cache.delete_pattern('*location_list*')