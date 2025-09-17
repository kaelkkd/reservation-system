from django.core.management.base import BaseCommand
from reserve.models import Location

SAMPLE_LOCATIONS = [
    {"name": "Downtown Hotel", "address_line": "123 Main St", "country": "US", "capacity": 10, "is_available": True},
    {"name": "Beachside Resort", "address_line": "45 Ocean Ave", "country": "US", "capacity": 15, "is_available": True},
    {"name": "Mountain Lodge", "address_line": "9 Alpine Rd", "country": "US", "capacity": 8, "is_available": True},
    {"name": "City Inn", "address_line": "77 Center Blvd", "country": "UK", "capacity": 12, "is_available": True},
    {"name": "Tokyo Stay", "address_line": "1-2-3 Shibuya", "country": "JP", "capacity": 14, "is_available": True},
]

class Command(BaseCommand):
    help = "Seed the database with sample Location records"

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Delete existing locations before seeding')

    def handle(self, *args, **options):
        if options.get('reset'):
            deleted, _ = Location.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing locations"))

        created_count = 0
        for data in SAMPLE_LOCATIONS:
            obj, created = Location.objects.get_or_create(
                name=data["name"],
                defaults=data,
            )
            created_count += 1 if created else 0
        self.stdout.write(self.style.SUCCESS(f"Seeded {created_count} new locations (total: {Location.objects.count()})"))
