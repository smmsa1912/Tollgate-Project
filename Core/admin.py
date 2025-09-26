from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("First_Name", "Last_Name", "Email", "Phone_Number")
    list_filter = ["is_active"]
    readonly_fields = ("password",)
    search_fields = ["First_Name", "Last_Name", "Email", "Phone_Number"]
    ordering = ["First_Name", "Last_Name"]
    fieldsets = [
        ("User Information",
         {"fields": ["First_Name", "Last_Name", "Email", "Phone_Number", "password"]}),
        ("Permissions", {"fields": ["is_superuser", "is_staff", "is_active"]}),
    ]


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("Car_Number", "RFID", "Owner")
    search_fields = ["Car_Number", "RFID", "Owner__Email"]
    ordering = ["Car_Number"]
    fieldsets = [
        ("Vehicle Information",
         {"fields": ["Car_Number", "RFID", "Owner"]}),
    ]


@admin.register(Exit_Point)
class ExitPointAdmin(admin.ModelAdmin):
    list_display = ("Exit_Point_ID", "Location", "Charges_Per_KM")
    search_fields = ["Exit_Point_ID", "Location"]
    ordering = ["Exit_Point_ID"]
    fieldsets = [
        ("Exit Point Information",
         {"fields": ["Exit_Point_ID", "Location", "Charges_Per_KM"]}),
    ]


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ("Camera_ID", "Location", "Latitude", "Longitude")
    search_fields = ["Camera_ID", "Location"]
    ordering = ["Camera_ID"]
    fieldsets = [
        ("Camera Information",
         {"fields": ["Camera_ID", "Location", "Latitude", "Longitude"]}),
    ]
