from django.core.management.base import BaseCommand
from Core.models import Exit_Point, Camera


class Command(BaseCommand):
    help = "Seed database with Cameras and Exit Points (with lat/lng)"

    def handle(self, *args, **kwargs):
        # Exit Points (example: real lat/lng)
        exit_points = [
            ("Mumbai Exit", 19.0760, 72.8777, 5.0),
            ("Pune Exit", 18.5204, 73.8567, 6.0),
            ("Nashik Exit", 19.9975, 73.7898, 4.5),
            ("Nagpur Exit", 21.1458, 79.0882, 5.5),
        ]

        for name, lat, lng, charge in exit_points:
            Exit_Point.objects.get_or_create(
                Location=name,
                Latitude=lat,
                Longitude=lng,
                Charges_Per_KM=charge
            )

        # Cameras (example near those exits)
        cameras = [
            ("Mumbai Camera 1", 19.075, 72.877),
            ("Pune Camera 1", 18.521, 73.857),
            ("Nashik Camera 1", 19.998, 73.788),
            ("Nagpur Camera 1", 21.146, 79.089),
        ]

        for name, lat, lng in cameras:
            Camera.objects.get_or_create(
                Location=name,
                Latitude=lat,
                Longitude=lng
            )

        self.stdout.write(self.style.SUCCESS("✅ Cameras & Exit Points seeded successfully!"))
