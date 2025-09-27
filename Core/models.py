from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from Core.manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50, blank=True)
    Email = models.EmailField("Email Address", unique=True)
    Phone_Number = models.CharField(max_length=10, unique=True)
    is_card_published = models.BooleanField(default=False)

    is_staff = models.BooleanField(('staff status'), default=False,
                                   help_text=('Designates whether the user can log into this admin '
                                              'site.'))
    is_active = models.BooleanField(('active'), default=True,
                                    help_text=('Designates whether this user should be treated as '
                                               'active. Unselect this instead of deleting accounts.'))
    is_superuser = models.BooleanField(('superuser status'), default=False,
                                       help_text=('Designates that this user has all permissions without '
                                                  'explicitly assigning them.'))

    USERNAME_FIELD = "Email"
    REQUIRED_FIELDS = ["First_Name", "Phone_Number"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.Email}"


class Exit_Point(models.Model):
    class Meta:
        verbose_name = "Exit Point"
        verbose_name_plural = "Exit Points"

    Exit_Point_ID = models.AutoField(primary_key=True)
    Charges_Per_KM = models.FloatField()
    Longitude = models.FloatField()
    Latitude = models.FloatField()
    Location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Exit Point {self.Exit_Point_ID} - {self.Location}"


class Camera(models.Model):
    class Meta:
        verbose_name = "Camera"
        verbose_name_plural = "Cameras"

    Camera_ID = models.AutoField(primary_key=True)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    Location = models.CharField(max_length=255)

    def __str__(self):
        return f"Camera {self.Camera_ID} - {self.Location}"


class Vehicle(models.Model):
    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    RFID = models.CharField(max_length=50, unique=True)
    Car_Number = models.CharField(max_length=20, unique=True)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")

    def __str__(self):
        return f"{self.Car_Number} - {self.Owner.Email}"


class VehicleEntry(models.Model):
    class Meta:
        verbose_name = "Vehicle Entry"
        verbose_name_plural = "Vehicle Entries"

    Entry_ID = models.AutoField(primary_key=True)
    Vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="entries", blank=True, null=True)
    Raw_Car_Number = models.CharField(max_length=10, blank=False)
    Entry_Camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="vehicle_entries")
    Entry_Time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.Vehicle:
            return f"Entry {self.Entry_ID} - {self.Vehicle.Car_Number} at {self.Entry_Time}"
        return f"Entry {self.Entry_ID} - {self.Raw_Car_Number} at {self.Entry_Time}"


class TollRecord(models.Model):
    Record_ID = models.AutoField(primary_key=True)

    Vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="toll_records", null=True, blank=True
    )
    Raw_Car_Number = models.CharField(max_length=20, blank=True, null=True)

    Entry_Point = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="toll_entries")
    Exit_Point = models.ForeignKey(Exit_Point, on_delete=models.CASCADE, related_name="toll_exits")
    Distance_Traveled_KM = models.FloatField()
    Toll_Charged = models.FloatField()
    Timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.Vehicle:
            return f"Toll {self.Exit_Point} - {self.Vehicle.Car_Number} charged {self.Toll_Charged}"
        return f"Toll {self.Exit_Point} - {self.Raw_Car_Number} charged {self.Toll_Charged}"
