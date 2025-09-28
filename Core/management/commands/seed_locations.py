from django.core.management.base import BaseCommand
from Core.models import Exit_Point, Camera


class Command(BaseCommand):
    help = "Seed database with realistic Cameras and Exit Points for major highways from Mumbai"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database with Camera and Exit Point data...")

        # Clear existing data to prevent duplicates on re-runs
        Camera.objects.all().delete()
        Exit_Point.objects.all().delete()

        self.stdout.write("Cleared old data.")

        # --- Data Seeding ---
        # The data is structured to represent logical entry cameras and exit toll plazas
        # on major highways radiating from the Mumbai Metropolitan Region.

        # 1. Mumbai-Pune Expressway (Yashwantrao Chavan Expressway)
        # One of the most important routes out of Mumbai.
        Exit_Point.objects.create(
            Location="Khalapur Main Toll Plaza, NH 48",
            Latitude=18.9135,  # Precise coordinate for the toll plaza
            Longitude=73.3032,
            Charges_Per_KM=3.20  # Approx. rate per km for cars
        )
        Camera.objects.create(
            Location="Panvel Entry Camera, Mumbai-Pune Expressway",
            Latitude=19.0185,  # Camera placed near the start of the expressway
            Longitude=73.1198,
        )

        # 2. Mumbai-Nashik Highway (NH 160)
        # Major route towards Northeast Maharashtra.
        Exit_Point.objects.create(
            Location="Ghoti Toll Plaza, NH 160",
            Latitude=19.7451,  # Toll plaza before Nashik
            Longitude=73.8694,
            Charges_Per_KM=2.80
        )
        Camera.objects.create(
            Location="Bhiwandi Bypass Camera, NH 160",
            Latitude=19.2899,  # Camera placed after Thane, on the way to Nashik
            Longitude=73.0655,
        )

        # 3. Mumbai-Ahmedabad Highway (NH 48)
        # The main artery north towards Gujarat.
        Exit_Point.objects.create(
            Location="Charoti Toll Plaza, Dahanu, NH 48",
            Latitude=20.0107,  # Major toll plaza on the way to Gujarat
            Longitude=72.9033,
            Charges_Per_KM=2.95
        )
        Camera.objects.create(
            Location="Vasai-Virar Bridge Camera, NH 48",
            Latitude=19.4578,  # Camera after crossing the Vasai creek bridge
            Longitude=72.8251,
        )

        # 4. Mumbai-Goa Highway (NH 66)
        # The scenic but busy route south along the Konkan coast.
        Exit_Point.objects.create(
            Location="Mangaon Toll Plaza, NH 66",
            Latitude=18.2683,  # A toll plaza on the route to Goa
            Longitude=73.2811,
            Charges_Per_KM=2.75
        )
        Camera.objects.create(
            Location="Pen Bypass Camera, NH 66",
            Latitude=18.7350,  # Camera placed after the town of Pen
            Longitude=73.1001,
        )

        # 5. Eastern Express Highway (Thane-Mumbai Entry)
        # One of the 5 entry points into Mumbai city.
        Exit_Point.objects.create(
            Location="Mulund East Toll Plaza, Eastern Express Highway",
            Latitude=19.1718,
            Longitude=72.9472,
            Charges_Per_KM=12.5  # Represents a flat entry fee
        )
        Camera.objects.create(
            Location="Thane (Majiwada Junction) Camera, Eastern Express Highway",
            Latitude=19.2183,
            Longitude=72.9781,
        )

        # 6. Sion-Panvel Highway (Navi Mumbai-Mumbai Entry)
        # The main entry point from Navi Mumbai.
        Exit_Point.objects.create(
            Location="Vashi Toll Plaza, Sion-Panvel Highway",
            Latitude=19.0681,
            Longitude=72.9972,
            Charges_Per_KM=14.0  # Represents a flat entry fee
        )
        Camera.objects.create(
            Location="Vashi (Sector 17) Camera, Navi Mumbai",
            Latitude=19.0833,
            Longitude=73.0033,
        )

        # 7. Bandra-Worli Sea Link (Intra-city Toll)
        # Iconic intra-city expressway.
        Exit_Point.objects.create(
            Location="Bandra-Worli Sea Link Toll Plaza (Worli Side)",
            Latitude=19.0288,
            Longitude=72.8168,
            Charges_Per_KM=15.0  # Represents a flat toll fee for the ~5.6km bridge
        )
        Camera.objects.create(
            Location="Bandra-Worli Sea Link Entry Camera (Bandra Side)",
            Latitude=19.0428,
            Longitude=72.8222,
        )

        self.stdout.write(self.style.SUCCESS(
            "✅ Successfully seeded 7 Cameras and 7 Exit Points with realistic, distant coordinates."
        ))

